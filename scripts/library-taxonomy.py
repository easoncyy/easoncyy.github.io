"""Library classification shared by catalog commands."""
CATEGORIES = ("文学", "哲学", "历史", "教材", "习题", "参考书", "其他")
ACADEMIC = ("教材", "习题", "参考书")


def classify(book):
    category = book.get("category", "其他")
    if category not in CATEGORIES:
        raise ValueError(f"未知图书分类：{category}")
    subject = str(book.get("subject", "")).strip()
    if category in ACADEMIC:
        subject = subject or "未分学科"
    elif subject:
        raise ValueError(f"{category} 不使用二级学科分类")
    return category, subject
