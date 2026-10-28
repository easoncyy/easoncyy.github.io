"""Local desktop manager. No server, public admin endpoint, or stored token."""
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from problem_store import ROOT, BANK, SCHEDULE, today, load_bank, load_schedule, save_problem, write_json, valid_id, trash_problem, restore_problem, problem_status
from library_panel import LibraryPanel

class Manager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('~/notes · 网站管理')
        self.geometry('1320x900'); self.minsize(1100,780)
        self.busy=False; self.events=queue.Queue(); self.current=None; self.photos=[]
        self.bank={}; self.day_ids=[]
        style=ttk.Style(self); style.theme_use('clam')
        style.configure('.',font=('Microsoft YaHei UI',10))
        style.configure('Heading.TLabel',font=('Microsoft YaHei UI',15,'bold'))
        style.configure('Muted.TLabel',foreground='#666666',font=('Microsoft YaHei UI',9))
        style.configure('TButton',padding=(12,7))
        style.configure('Primary.TButton',background='#202020',foreground='white',padding=(14,8))
        style.map('Primary.TButton',background=[('active','#444444')],foreground=[('active','white')])
        style.configure('Treeview',rowheight=32)
        style.configure('Treeview.Heading',padding=(6,8),font=('Microsoft YaHei UI',10,'bold'))
        ttk.Label(self,text='~/notes  /  网站管理',style='Heading.TLabel',padding=(18,14,18,0)).pack(anchor='w')
        tabs=ttk.Notebook(self); tabs.pack(fill='both',expand=True,padx=12,pady=12)
        self.problem_tab=ttk.Frame(tabs,padding=12); tabs.add(self.problem_tab,text='题库编辑')
        self.schedule_tab=ttk.Frame(tabs,padding=12); tabs.add(self.schedule_tab,text='每日排期')
        self.content_tab=ttk.Frame(tabs,padding=12); tabs.add(self.content_tab,text='日志')
        self.library_tab=LibraryPanel(tabs,self);tabs.add(self.library_tab,text='图书馆')
        self.publish_tab=ttk.Frame(tabs,padding=12); tabs.add(self.publish_tab,text='构建与发布')
        self.make_bank(); self.make_schedule(); self.make_content(); self.make_publish()
        self.status=tk.StringVar(value='修改保存在本地；点击“构建并发布网站”后才会更新到线上。')
        ttk.Label(self,textvariable=self.status,padding=(15,4)).pack(fill='x')
        self.refresh(); self.new_problem(); self.load_day(); self.after(150,self.poll)
        self.protocol('WM_DELETE_WINDOW',self.close)

    def guard(self):
        if self.busy: raise ValueError('构建或发布中，请等待任务完成后再修改文件。')

    def safely(self, action):
        try: action()
        except Exception as error: messagebox.showerror('操作未完成',str(error),parent=self)

    def backup(self,path):
        if path.exists():
            folder=ROOT/'tmp/manager-backups'; folder.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,folder/(datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'-'+path.name))

    def make_bank(self):
        pane=ttk.Panedwindow(self.problem_tab,orient='horizontal'); pane.pack(fill='both',expand=True)
        left=ttk.Frame(pane); right=ttk.Frame(pane,padding=(14,0)); pane.add(left,weight=1); pane.add(right,weight=3)
        self.bank_tree=ttk.Treeview(left,columns=('title','state','schedule','dates'),show='headings',selectmode='browse')
        self.bank_tree.heading('title',text='题目');self.bank_tree.heading('state',text='内容状态');self.bank_tree.heading('schedule',text='排期情况')
        self.bank_tree.column('title',width=210,minwidth=120);self.bank_tree.column('state',width=75,minwidth=70);self.bank_tree.column('schedule',width=95,minwidth=80)
        self.bank_tree.heading('dates',text='已保存日期');self.bank_tree.column('dates',width=120,minwidth=90)
        self.bank_tree.pack(fill='both',expand=True)
        self.bank_tree.bind('<<TreeviewSelect>>',lambda _:self.select_problem())
        bar=ttk.Frame(left);bar.pack(fill='x',pady=8)
        ttk.Button(bar,text='新建题目',command=self.new_problem).pack(side='left')
        ttk.Button(bar,text='刷新',command=lambda:self.safely(self.refresh)).pack(side='left',padx=5)
        deletion=ttk.Frame(left);deletion.pack(fill='x')
        ttk.Button(deletion,text='删除题目',command=lambda:self.safely(self.delete_question)).pack(side='left')
        ttk.Button(deletion,text='从回收站恢复',command=lambda:self.safely(self.restore_question)).pack(side='left',padx=5)
        self.fields={}
        for row,(key,label) in enumerate([('id','ID（英文、数字、连字符）'),('title','题目标题'),('path','分类目录（用 / 分隔）'),('tags','标签（逗号分隔）'),('source','来源 / 出处')]):
            ttk.Label(right,text=label).grid(row=row,column=0,sticky='w',pady=3)
            value=tk.StringVar();self.fields[key]=value
            ttk.Entry(right,textvariable=value).grid(row=row,column=1,sticky='ew',pady=3)
        self.draft=tk.BooleanVar(value=False)
        ttk.Checkbutton(right,text='草稿：允许未写完，保存后暂不允许排期',variable=self.draft).grid(row=5,column=1,sticky='w')
        ttk.Label(right,text='题目正文 · Markdown / $行内公式$ / $$独立公式$$').grid(row=6,column=0,columnspan=2,sticky='w',pady=(10,3))
        self.question=ScrolledText(right,height=8,undo=True,font=('Consolas',11));self.question.grid(row=7,column=0,columnspan=2,sticky='nsew')
        ttk.Label(right,text='答案与解析 · 网页默认折叠').grid(row=8,column=0,columnspan=2,sticky='w',pady=(10,3))
        self.answer=ScrolledText(right,height=8,undo=True,font=('Consolas',11));self.answer.grid(row=9,column=0,columnspan=2,sticky='nsew')
        ttk.Button(right,text='保存题目到本地',command=lambda:self.safely(self.save_question)).grid(row=10,column=0,columnspan=2,sticky='e',pady=8)
        right.columnconfigure(1,weight=1);right.rowconfigure(7,weight=1);right.rowconfigure(9,weight=1)

    def new_problem(self):
        self.current=None
        self.bank_tree.selection_remove(self.bank_tree.selection())
        for key,v in self.fields.items(): v.set('')
        self.fields['id'].set('p-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
        self.fields['path'].set('MATH/LINEAR-ALGEBRA')
        self.draft.set(True);self.question.delete('1.0','end');self.answer.delete('1.0','end')

    def select_problem(self):
        selected=self.bank_tree.selection()
        if not selected:return
        item=self.bank[selected[0]];self.current=item['id']
        for key,value in [('id',item['id']),('title',item['title']),('path','/'.join(item['path'])),('tags',', '.join(item['tags'])),('source',item['source'])]:self.fields[key].set(value)
        self.draft.set(item['draft'])
        for widget,value in [(self.question,item['question']),(self.answer,item['answer'])]:widget.delete('1.0','end');widget.insert('1.0',value)

    def save_question(self):
        self.guard();slug=valid_id(self.fields['id'].get().strip())
        if slug in self.bank and slug!=self.current and not messagebox.askyesno('覆盖题目','这个 ID 已存在，是否覆盖？',parent=self):return
        if self.draft.get() and any(slug in ids for ids in load_schedule().values()):raise ValueError('这道题已排期，请先从排期移除再改为草稿。')
        self.backup(BANK/(slug+'.qmd'))
        save_problem(slug,self.fields['title'].get(),[p.strip() for p in self.fields['path'].get().split('/')],
                     [t.strip() for t in self.fields['tags'].get().replace('，',',').split(',') if t.strip()],
                     self.question.get('1.0','end'),self.answer.get('1.0','end'),self.fields['source'].get(),self.draft.get())
        self.current=slug;self.refresh();self.status.set('题目已保存到本地；去“每日排期”安排日期，再发布。')

    def refresh(self):
        day=self.schedule_date.get().strip()
        pending=self.day_ids!=getattr(self,'schedule',{}).get(day,[])
        self.bank=load_bank();self.schedule=load_schedule(self.bank)
        self.bank_tree.delete(*self.bank_tree.get_children())
        for slug,item in self.bank.items():
            state,progress,dates=problem_status(item,self.schedule)
            self.bank_tree.insert('', 'end',iid=slug,values=(item['title'],state,progress,', '.join(dates) or '—'))
        self.available.delete(*self.available.get_children())
        for slug,item in self.bank.items():
            if item['draft']:continue
            state,progress,dates=problem_status(item,self.schedule)
            self.available.insert('', 'end',iid=slug,values=(item['title'],state,progress,', '.join(dates) or '—'))
        self.scheduled_days['values']=sorted(self.schedule.keys(),reverse=True)
        # Saved metadata updates both lists. Keep any unsaved daily ordering,
        # removing only entries that are no longer eligible for scheduling.
        if not pending:self.day_ids=list(self.schedule.get(day,[]))
        self.day_ids=[slug for slug in self.day_ids if slug in self.bank and not self.bank[slug]['draft']]
        self.draw_day()
        self.library_tab.refresh()

    def delete_question(self):
        self.guard();selected=self.bank_tree.selection()
        if not selected:raise ValueError('请先从左侧列表选择要删除的题目')
        slug=selected[0];schedule=load_schedule(self.bank);days=[day for day,ids in schedule.items() if slug in ids]
        detail='\n涉及排期：'+', '.join(sorted(days)) if days else '\n这道题尚未排期。'
        if not messagebox.askyesno('删除题目',f'将“{self.bank[slug]["title"]}”移至本地回收站？{detail}\n\n同时从所有日期移除；已上线内容需再次发布后才会移除。可从回收站恢复。',parent=self):return
        self.backup(SCHEDULE);trash_problem(slug);self.refresh();self.load_day();self.new_problem()
        self.status.set('题目已移至本地回收站，排期引用已移除。线上删除需重新发布。')

    def restore_question(self):
        self.guard();folder=ROOT/'archive/problem-trash';folder.mkdir(parents=True,exist_ok=True)
        name=filedialog.askopenfilename(parent=self,title='进入回收站日期文件夹，选择要恢复的题目',initialdir=folder,filetypes=[('题目','*.qmd')])
        if not name:return
        target=restore_problem(name);self.refresh();self.bank_tree.selection_set(target.stem);self.bank_tree.see(target.stem);self.select_problem()
        self.status.set('题目已恢复到题库；原排期不自动恢复，请重新安排日期。')

    def make_schedule(self):
        frame=self.schedule_tab
        ttk.Label(frame,text='每天可以安排任意数量的题目；空列表表示这一天不发布。排期保存后需发布一次，云端才会收到未来安排。').pack(anchor='w')
        bar=ttk.Frame(frame);bar.pack(fill='x',pady=12)
        self.schedule_date=tk.StringVar(value=today())
        ttk.Label(bar,text='日期 YYYY-MM-DD').pack(side='left')
        ttk.Entry(bar,textvariable=self.schedule_date,width=15).pack(side='left',padx=8)
        ttk.Button(bar,text='载入该日',command=lambda:self.safely(self.load_day)).pack(side='left')
        ttk.Label(bar,text='  已有排期').pack(side='left')
        self.scheduled_days=ttk.Combobox(bar,width=15,state='readonly');self.scheduled_days.pack(side='left',padx=8)
        self.scheduled_days.bind('<<ComboboxSelected>>',lambda _:self.choose_day())
        columns=ttk.Frame(frame);columns.pack(fill='both',expand=True)
        left=ttk.LabelFrame(columns,text='可用题库 · 可多选',padding=8);left.pack(side='left',fill='both',expand=True)
        self.available=ttk.Treeview(left,columns=('title','state','schedule','dates'),show='headings',selectmode='extended')
        for key,label,width in [('title','题目',210),('state','内容状态',75),('schedule','排期情况',100),('dates','已保存日期',150)]:
            self.available.heading(key,text=label);self.available.column(key,width=width,minwidth=70)
        self.available.pack(fill='both',expand=True)
        ttk.Button(left,text='加入当天 →',command=self.add_day_items).pack(pady=8)
        right=ttk.LabelFrame(columns,text='当天题目 · 显示顺序',padding=8);right.pack(side='left',fill='both',expand=True,padx=(12,0))
        self.chosen=tk.Listbox(right,exportselection=False,font=('Microsoft YaHei UI',10));self.chosen.pack(fill='both',expand=True)
        row=ttk.Frame(right);row.pack(pady=8)
        for text,action in [('移除',self.remove_day_item),('上移',lambda:self.move_day_item(-1)),('下移',lambda:self.move_day_item(1))]:ttk.Button(row,text=text,command=action).pack(side='left',padx=3)
        ttk.Button(frame,text='保存当天排期',command=lambda:self.safely(self.save_day)).pack(anchor='e',pady=12)
        self.day_summary=tk.StringVar()
        ttk.Label(frame,textvariable=self.day_summary,style='Muted.TLabel').pack(anchor='w')

    def choose_day(self):self.schedule_date.set(self.scheduled_days.get());self.safely(self.load_day)
    def load_day(self):self.day_ids=list(load_schedule(self.bank).get(self.schedule_date.get().strip(),[]));self.draw_day()
    def draw_day(self):
        self.chosen.delete(0,'end')
        for i,slug in enumerate(self.day_ids,1):self.chosen.insert('end',f'{i:02d}. '+self.bank[slug]['title'])
        day=self.schedule_date.get().strip();saved=getattr(self,'schedule',{}).get(day,[])
        state='已保存，两页排期状态已同步' if self.day_ids==saved else '有未保存调整，保存后同步到题库列表'
        self.day_summary.set(f'{day} · {len(self.day_ids)} 道题 · {state}')
    def add_day_items(self):
        for slug in self.available.selection():
            if slug not in self.day_ids:self.day_ids.append(slug)
        self.draw_day()
    def remove_day_item(self):
        if self.chosen.curselection():self.day_ids.pop(self.chosen.curselection()[0]);self.draw_day()
    def move_day_item(self,delta):
        if not self.chosen.curselection():return
        i=self.chosen.curselection()[0];j=i+delta
        if 0<=j<len(self.day_ids):self.day_ids[i],self.day_ids[j]=self.day_ids[j],self.day_ids[i];self.draw_day();self.chosen.selection_set(j)
    def save_day(self):
        from datetime import date
        self.guard();day=self.schedule_date.get().strip()
        if date.fromisoformat(day).isoformat()!=day:raise ValueError('日期格式必须是 YYYY-MM-DD')
        data=load_schedule(self.bank)
        if day in data and not messagebox.askyesno('更新排期',f'覆盖 {day} 的排期为 {len(self.day_ids)} 道题？',parent=self):return
        data[day]=list(self.day_ids);self.backup(SCHEDULE);write_json(SCHEDULE,data);self.refresh()
        self.status.set(f'已保存 {day}：{len(self.day_ids)} 道题。请发布一次以同步云端排期。')

    def make_content(self):
        frame=self.content_tab
        log=ttk.LabelFrame(frame,text='新建日志',padding=12);log.pack(fill='both',expand=True)
        self.log_title=tk.StringVar();ttk.Entry(log,textvariable=self.log_title).pack(fill='x')
        self.log_text=ScrolledText(log,height=7,font=('Microsoft YaHei UI',10));self.log_text.pack(fill='both',expand=True,pady=8)
        row=ttk.Frame(log);row.pack(fill='x')
        ttk.Button(row,text='选择照片（可多选）',command=self.choose_photos).pack(side='left')
        self.photo_label=ttk.Label(row,text='0 张');self.photo_label.pack(side='left',padx=10)
        ttk.Button(row,text='创建日志',command=lambda:self.safely(self.create_log)).pack(side='right')
        row=ttk.Frame(frame);row.pack(fill='x')
        ttk.Button(row,text='打开博客文件夹',command=lambda:os.startfile(ROOT/'posts')).pack(side='left')
        ttk.Button(row,text='打开日志文件夹',command=lambda:os.startfile(ROOT/'logs')).pack(side='left',padx=8)
        ttk.Button(row,text='打开网站目录',command=lambda:os.startfile(ROOT)).pack(side='left')
    def choose_photos(self):
        self.photos=list(filedialog.askopenfilenames(parent=self,title='选择日志照片',filetypes=[('照片','*.jpg *.jpeg *.png *.webp *.gif *.avif')]))
        self.photo_label.config(text=f'{len(self.photos)} 张')
    def create_log(self):
        self.guard()
        args=[sys.executable,str(ROOT/'scripts/new-log.py'),self.log_title.get(),'--text',self.log_text.get('1.0','end').strip()]
        if self.photos:args+=['--photo',*self.photos]
        self.run_job(args,'创建日志')

    def make_publish(self):
        frame=self.publish_tab
        ttk.Label(frame,text='发布会先本地构建，提交并推送当前仓库的所有修改，再由 GitHub Actions 构建部署。').pack(anchor='w')
        self.message=tk.StringVar(value='Update personal website')
        ttk.Entry(frame,textvariable=self.message).pack(fill='x',pady=10)
        row=ttk.Frame(frame);row.pack(fill='x')
        ttk.Button(row,text='只构建本地网页',command=lambda:self.safely(lambda:self.run_powershell('build.ps1',['-SkipPdf'],'构建网页'))).pack(side='left')
        ttk.Button(row,text='打开本地预览',command=lambda:self.safely(self.preview)).pack(side='left',padx=8)
        ttk.Button(row,text='构建并发布网站',command=lambda:self.safely(self.publish)).pack(side='left')
        ttk.Button(row,text='重试云端部署',command=lambda:self.safely(lambda:self.run_job([sys.executable,str(ROOT/'scripts/publish-github.py')],'提交云端部署'))).pack(side='left',padx=8)
        ttk.Button(row,text='查看线上网站',command=lambda:webbrowser.open('https://easoncyy.github.io/problems.html')).pack(side='left',padx=8)
        ttk.Button(row,text='查看部署状态',command=lambda:webbrowser.open('https://github.com/easoncyy/easoncyy.github.io/actions')).pack(side='left')
        ttk.Label(frame,text='每日 00:05 会重新构建 main 上的整个网站（含博客、日志和图书馆）。只在本地保存的改动不会自动上传。',wraplength=1000).pack(anchor='w',pady=10)
        self.output=ScrolledText(frame,font=('Consolas',10),state='disabled');self.output.pack(fill='both',expand=True)
    def powershell(self):return shutil.which('pwsh') or shutil.which('powershell') or 'powershell.exe'
    def run_powershell(self,script,args,title):self.run_job([self.powershell(),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts'/script),*args],title)
    def publish(self):
        self.guard()
        if messagebox.askyesno('发布当前网站','这会将当前仓库中所有修改和新增文件公开推送到 GitHub。确认发布？',parent=self):
            self.run_powershell('deploy.ps1',['-Message',self.message.get().strip() or 'Update personal website'],'构建并发布')
    def preview(self):
        self.guard();site=ROOT/'_site'
        if not (site/'index.html').exists():raise ValueError('请先点击“只构建本地网页”。')
        self.preview_process=getattr(self,'preview_process',None)
        if self.preview_process is None or self.preview_process.poll() is not None:
            self.preview_process=subprocess.Popen([sys.executable,'-m','http.server','4280','--bind','127.0.0.1','--directory',str(site)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        webbrowser.open('http://127.0.0.1:4280/problems.html')
    def run_job(self,args,title):
        self.guard();self.busy=True;self.status.set(title+'中…')
        def worker():
            try:
                env=os.environ.copy();env['PYTHONIOENCODING']='utf-8';env['PYTHONUTF8']='1'
                python_dir=str(Path(sys.executable).parent)
                env['PATH']=python_dir+os.pathsep+env.get('PATH','')
                args[0]=str(Path(sys.executable).with_name('python.exe')) if args[0]==sys.executable and sys.executable.lower().endswith('pythonw.exe') else args[0]
                process=subprocess.Popen(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                translation_notice = False
                self.events.put(('line', '\n--- '+title+' ---\n'))
                for line in process.stdout:
                    if ('Could not load translations for zh-CN' in line
                            or line.strip() == 'translations/zh.yaml:'
                            or 'The term Abstract has no translation defined.' in line):
                        if not translation_notice:
                            self.events.put(('line', '[说明] Quarto 缺少部分中文翻译，不影响构建。重复提示已合并。\n'))
                            translation_notice = True
                        continue
                    self.events.put(('line',line))
                code=process.wait();self.events.put(('done',(code,title)))
            except Exception as error:self.events.put(('line',str(error)+'\n'));self.events.put(('done',(1,title)))
        threading.Thread(target=worker,daemon=True).start()
    def poll(self):
        try:
            while True:
                kind,value=self.events.get_nowait()
                if kind=='line':self.output.config(state='normal');self.output.insert('end',value);self.output.see('end');self.output.config(state='disabled')
                else:
                    code,title=value;self.busy=False;self.status.set(title+('已完成。发布任务完成后仍需等待 Pages 部署。' if code==0 else '失败，请查看“构建与发布”日志。'))
                    if code:messagebox.showerror('任务失败','请查看“构建与发布”页的日志。',parent=self)
        except queue.Empty:pass
        self.after(150,self.poll)
    def close(self):
        if self.busy:messagebox.showinfo('任务正在执行','请等待任务完成再关闭窗口。',parent=self);return
        process=getattr(self,'preview_process',None)
        if process and process.poll() is None:process.terminate()
        self.destroy()

if __name__=='__main__':
    try:Manager().mainloop()
    except Exception as error:
        root=tk.Tk();root.withdraw();messagebox.showerror('网站管理启动失败',str(error));root.destroy()
