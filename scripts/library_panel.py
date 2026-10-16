"""Dedicated library workspace for the local site manager."""
import os
import re
import webbrowser
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog
from tkinter.scrolledtext import ScrolledText
from library_store import ROOT,taxonomy,STATES,load_books,load_reading,save_book,save_reading,validate_file

class LibraryPanel(ttk.Frame):
    def __init__(self,parent,manager):
        super().__init__(parent,padding=16);self.manager=manager;self.current=None;self.local_file=None
        header=ttk.Frame(self);header.pack(fill='x',pady=(0,14))
        ttk.Label(header,text='library/ 图书馆',style='Heading.TLabel').pack(side='left')
        ttk.Button(header,text='＋ 添加书目',command=lambda:manager.safely(self.new_book),style='Primary.TButton').pack(side='right')
        ttk.Button(header,text='刷新书架',command=lambda:manager.safely(self.refresh)).pack(side='right',padx=8)
        pane=ttk.Panedwindow(self,orient='horizontal');pane.pack(fill='both',expand=True)
        left=ttk.Frame(pane);right=ttk.Frame(pane,padding=(20,0,0,0));pane.add(left,weight=3);pane.add(right,weight=4)
        filter_bar=ttk.Frame(left);filter_bar.pack(fill='x',pady=(0,10))
        self.search=tk.StringVar();ttk.Entry(filter_bar,textvariable=self.search).pack(side='left',fill='x',expand=True)
        self.state_filter=ttk.Combobox(filter_bar,values=['全部状态',*STATES],state='readonly',width=13);self.state_filter.set('全部状态');self.state_filter.pack(side='left',padx=(8,0))
        self.search.trace_add('write',lambda *_:self.draw_books());self.state_filter.bind('<<ComboboxSelected>>',lambda _:self.draw_books())
        ttk.Label(left,text='搜索书名 / 作者 / 分类',style='Muted.TLabel').pack(anchor='w',pady=(0,6))
        table=ttk.Frame(left);table.pack(fill='both',expand=True)
        self.tree=ttk.Treeview(table,columns=('title','category','state'),show='headings',selectmode='browse')
        for key,label,width in [('title','书名',245),('category','分类',85),('state','书单状态',90)]:self.tree.heading(key,text=label);self.tree.column(key,width=width,minwidth=65)
        scroll=ttk.Scrollbar(table,orient='vertical',command=self.tree.yview);self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
        self.tree.bind('<<TreeviewSelect>>',lambda _:manager.safely(self.select_book))
        self.summary=tk.StringVar();ttk.Label(left,textvariable=self.summary,style='Muted.TLabel').pack(anchor='w',pady=10)
        self.editor_title=tk.StringVar(value='选择左侧图书，或添加新书')
        ttk.Label(right,textvariable=self.editor_title,style='Heading.TLabel',wraplength=440).pack(anchor='w',pady=(0,10))
        tabs=ttk.Notebook(right);tabs.pack(fill='both',expand=True)
        info=ttk.Frame(tabs,padding=14);reading=ttk.Frame(tabs,padding=14)
        tabs.add(info,text='书目信息与文件');tabs.add(reading,text='书单与阅读状态')
        self.fields={}
        for row,(key,label) in enumerate([('slug','书目 ID'),('title','书名'),('author','作者')]):
            ttk.Label(info,text=label).grid(row=row,column=0,sticky='w',pady=5)
            variable=tk.StringVar();self.fields[key]=variable;entry=ttk.Entry(info,textvariable=variable);entry.grid(row=row,column=1,sticky='ew',pady=5)
            if key=='slug':self.slug_entry=entry
        for row,(key,label,options) in enumerate([('category','分类',taxonomy.CATEGORIES),('subject','学科（教材等）',('数学','计算机','人工智能','物理','法学'))],3):
            ttk.Label(info,text=label).grid(row=row,column=0,sticky='w',pady=5)
            self.fields[key]=tk.StringVar()
            combo=ttk.Combobox(info,textvariable=self.fields[key],values=options,state='readonly' if key=='category' else 'normal');combo.grid(row=row,column=1,sticky='ew',pady=5)
            if key=='category':combo.bind('<<ComboboxSelected>>',lambda _:self.category_changed())
        ttk.Label(info,text='简介').grid(row=5,column=0,sticky='nw',pady=5)
        self.description=ScrolledText(info,height=4,wrap='word',font=('Microsoft YaHei UI',10));self.description.grid(row=5,column=1,sticky='nsew',pady=5)
        files=ttk.LabelFrame(info,text='文件 · PDF / EPUB',padding=10);files.grid(row=6,column=0,columnspan=2,sticky='ew',pady=12)
        self.file_label=tk.StringVar(value='尚未选择文件')
        ttk.Label(files,textvariable=self.file_label,wraplength=400,style='Muted.TLabel').pack(anchor='w')
        file_bar=ttk.Frame(files);file_bar.pack(fill='x',pady=(8,0))
        ttk.Button(file_bar,text='选择 / 替换文件',command=lambda:manager.safely(self.choose_file)).pack(side='left')
        ttk.Button(file_bar,text='打开当前文件',command=lambda:manager.safely(self.open_file)).pack(side='left',padx=8)
        ttk.Label(info,text='或填写外部文件链接（如 Release 下载地址）',style='Muted.TLabel').grid(row=7,column=0,columnspan=2,sticky='w')
        self.fields['url']=tk.StringVar();ttk.Entry(info,textvariable=self.fields['url']).grid(row=8,column=0,columnspan=2,sticky='ew',pady=5)
        self.book_format=ttk.Combobox(info,values=['pdf','epub'],state='readonly',width=8);self.book_format.set('pdf');self.book_format.grid(row=9,column=0,sticky='w')
        ttk.Button(info,text='保存书目到本地',style='Primary.TButton',command=lambda:manager.safely(self.save_book)).grid(row=9,column=1,sticky='e',pady=8)
        info.columnconfigure(1,weight=1);info.rowconfigure(5,weight=1)
        ttk.Label(reading,text='按书单分别设置状态和备注。',style='Muted.TLabel').pack(anchor='w',pady=(0,14))
        self.list_id=tk.StringVar(value='personal');self.list_title=tk.StringVar(value='我的书单')
        ttk.Label(reading,text='书单 ID（选择已有，或输入新的英文 ID）').pack(anchor='w')
        self.list_combo=ttk.Combobox(reading,textvariable=self.list_id);self.list_combo.pack(fill='x',pady=(4,10));self.list_combo.bind('<<ComboboxSelected>>',lambda _:self.load_state())
        ttk.Label(reading,text='书单名称').pack(anchor='w');ttk.Entry(reading,textvariable=self.list_title).pack(fill='x',pady=(4,10))
        ttk.Label(reading,text='阅读状态').pack(anchor='w')
        self.reading_state=ttk.Combobox(reading,state='readonly',values=list(STATES));self.reading_state.set('未加入书单');self.reading_state.pack(fill='x',pady=(4,10))
        ttk.Label(reading,text='阅读备注 / 推荐语').pack(anchor='w')
        self.note=ScrolledText(reading,height=6,wrap='word',font=('Microsoft YaHei UI',10));self.note.pack(fill='both',expand=True,pady=(4,12))
        ttk.Button(reading,text='保存书单状态',style='Primary.TButton',command=lambda:manager.safely(self.save_state)).pack(anchor='e')
        ttk.Label(right,text='保存仅修改本地文件；在“构建与发布”中预览或上线。',style='Muted.TLabel').pack(anchor='w',pady=(12,0))
        self.refresh()

    def refresh(self):
        self.books=load_books();self.reading=load_reading();self.list_combo['values']=[x['id'] for x in self.reading['lists']];self.draw_books()
    def state_for(self,slug):
        states={x['status'] for listing in self.reading['lists'] for x in listing['items'] if x.get('book')==slug}
        return next((label for label,state in STATES.items() if state and state in states),'未加入书单')
    def draw_books(self):
        if not hasattr(self,'tree') or not hasattr(self,'books'):return
        self.tree.delete(*self.tree.get_children());query=self.search.get().strip().casefold();count=0
        for book in self.books:
            state=self.state_for(book['slug'])
            if query and query not in ' '.join(str(book.get(k,'')) for k in ['title','author','category','subject']).casefold():continue
            if self.state_filter.get() not in ('全部状态',state):continue
            self.tree.insert('','end',iid=book['slug'],values=(book['title'],book['category'],state));count+=1
        self.summary.set(f'{len(self.books)} 本图书 · 显示 {count} 本')
    def category_changed(self):
        if self.fields['category'].get() not in taxonomy.ACADEMIC:self.fields['subject'].set('')
    def new_book(self):
        self.manager.guard();self.current=None;self.local_file=None;self.editor_title.set('添加新书')
        self.tree.selection_remove(self.tree.selection());self.slug_entry.configure(state='normal')
        for variable in self.fields.values():variable.set('')
        self.fields['slug'].set('book-'+datetime.now().strftime('%Y%m%d-%H%M%S'));self.fields['category'].set('其他')
        self.description.delete('1.0','end');self.file_label.set('选择本地 PDF / EPUB，或填写外部文件链接');self.book_format.set('pdf')
        self.note.delete('1.0','end');self.reading_state.set('未加入书单')
    def select_book(self):
        selected=self.tree.selection()
        if not selected:return
        book=next(b for b in self.books if b['slug']==selected[0]);self.current=book['slug'];self.local_file=None
        self.editor_title.set(book['title']);self.slug_entry.configure(state='readonly')
        for key,variable in self.fields.items():variable.set(book.get(key,'') if key!='url' else (book['path'] if book['path'].startswith('http') else ''))
        self.description.delete('1.0','end');self.description.insert('1.0',book.get('description',''))
        self.file_label.set(book['path']);self.book_format.set(book.get('format',Path(book['path']).suffix[1:] or 'pdf'))
        self.load_state()
    def choose_file(self):
        self.manager.guard();name=filedialog.askopenfilename(parent=self,title='导入 PDF / EPUB',filetypes=[('电子书','*.pdf *.epub'),('PDF','*.pdf'),('EPUB','*.epub')])
        if not name:return
        file=validate_file(name);self.local_file=file;self.file_label.set(file.name+f' · {file.stat().st_size/1048576:.1f} MB');self.book_format.set(file.suffix[1:].lower())
        if not self.current:
            if not self.fields['title'].get():self.fields['title'].set(file.stem)
            slug=re.sub('[^a-z0-9]+','-',file.stem.lower()).strip('-')
            if slug:self.fields['slug'].set(slug)
        self.fields['url'].set('')
    def save_book(self):
        self.manager.guard();values={k:v.get() for k,v in self.fields.items()};values['description']=self.description.get('1.0','end').strip();values['format']=self.book_format.get()
        book=save_book(values,self.current,self.local_file,self.manager.backup);self.current=book['slug'];self.local_file=None
        self.search.set('');self.state_filter.set('全部状态');self.refresh();self.tree.selection_set(self.current);self.tree.see(self.current);self.select_book()
        self.manager.status.set('书目已保存；本地文件已复制到 assets/library。可继续设置书单状态，再构建预览。')
    def load_state(self):
        listing=next((x for x in self.reading['lists'] if x['id']==self.list_id.get()),None)
        item=next((x for x in listing['items'] if x.get('book')==self.current),None) if listing else None
        self.list_title.set(listing['title'] if listing else '')
        self.reading_state.set(next((k for k,v in STATES.items() if v==(item or {}).get('status','')),'未加入书单'))
        self.note.delete('1.0','end');self.note.insert('1.0',(item or {}).get('note',''))
    def save_state(self):
        self.manager.guard()
        if not self.current:raise ValueError('请先保存书目，或从左侧选择一本书')
        slug=self.current
        save_reading(slug,self.list_id.get().strip(),self.list_title.get(),STATES[self.reading_state.get()],self.note.get('1.0','end').strip(),self.manager.backup)
        self.refresh()
        if self.tree.exists(slug):self.tree.selection_set(slug)
        self.manager.status.set('书单状态已保存到本地。')
    def open_file(self):
        if self.local_file:os.startfile(self.local_file);return
        if not self.current:raise ValueError('请先选择图书')
        book=next(b for b in self.books if b['slug']==self.current)
        if book['path'].startswith('http'):webbrowser.open(book['path'])
        else:os.startfile(ROOT/book['path'].lstrip('/'))
