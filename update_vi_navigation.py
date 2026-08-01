import os
import re

# Vietnamese chapters in order
vi_chapters = [
    ("chuong-01-van-de", "Vấn Đề"),
    ("chuong-02-cong-cu", "Công Cụ"),
    ("chuong-03-su-chinh-xac", "Sự Chính Xác"),
    ("chuong-04-ket-qua", "Kết Quả"),
    ("chuong-05-kho-nang-luong", "Kho Năng Lượng"),
    ("chuong-06-he-truyen-dat", "Hệ Truyền Đạt"),
    ("chuong-07-he-thong-core", "Hệ Thống CORE"),
    ("chuong-08-quiet-eye", "Quiet Eye"),
    ("chuong-09-on-dinh-tien-dinh", "Ổn Định Tiền Đình"),
    ("chuong-10-fascia-ban-the-cam", "Fascia & Bản Thể Cảm"),
    ("chuong-11-tensegrity", "Tensegrity"),
    ("chuong-12-chu-ky-cang-rut", "Chu Kỳ Co Giãn"),
    ("chuong-13-dieu-tiet-figure-8", "Điều Tiết Figure-8"),
    ("chuong-14-mat-phang-45-do", "Mặt Phẳng 45°"),
    ("chuong-15-phanh-va-xung", "Phanh Và Xung"),
    ("chuong-16-jin", "Jin (Nội Lực)"),
    ("chuong-17-buoc-chan-hu-thuc", "Bước Chân Hư Thực"),
    ("chuong-18-ben-re", "Bén Rễ (Rooting)"),
    ("chuong-19-he-thong-forehand-push", "Hệ Thống Forehand Push"),
    ("chuong-20-backhand-saber-mot-tay", "Backhand Saber 1 Tay"),
    ("chuong-21-backhand-hai-tay-dang-lai", "Backhand 2 Tay Dạng Lai"),
    ("chuong-22-giao-bong", "Kỹ Thuật Giao Bóng"),
    ("chuong-23-do-giao-bong", "Đỡ Giao Bóng"),
    ("chuong-24-vo-le-va-overhead", "Vô-Lê & Overhead"),
    ("chuong-25-slice-drop-shot-va-lob", "Slice, Drop Shot & Lob"),
    ("chuong-26-hinh-hoc-san", "Hình Học Sân"),
    ("chuong-27-pattern-don-va-he-thong-doi", "Pattern Đơn & Đôi"),
    ("chuong-28-tam-ly", "Tâm Lý Thi Đấu"),
    ("chuong-29-the-chat", "Thể Chất Tennis"),
    ("chuong-30-he-thong-thong-nhat", "Hệ Thống Thống Nhất"),
]

base_path = r"C:\Users\Henry\Documents\Github Repos\tenniskb-repo\vi\chuong"

def generate_nav_html(chapter_idx):
    """Generate the navigation HTML for a chapter."""
    prev_slug = vi_chapters[chapter_idx-1][0] if chapter_idx > 0 else None
    next_slug = vi_chapters[chapter_idx+1][0] if chapter_idx < len(vi_chapters)-1 else None
    
    nav_parts = []
    
    # Previous link
    if prev_slug:
        prev_title = vi_chapters[chapter_idx-1][1]
        nav_parts.append(f'''<a href="../{prev_slug}/" class="md-footer__link" style="display: inline-flex; align-items: center; text-decoration: none; color: #2e7d32; font-weight: 500; padding: 0.6rem 1.2rem; border: 1.5px solid #2e7d32; border-radius: 6px; background: #f8f9fa;"><span style="font-size: 1.2rem; margin-right: 0.5rem; font-weight: bold;">←</span><span style="display: flex; flex-direction: column;"><span style="font-size: 0.7rem; text-transform: uppercase; color: #666; letter-spacing: 0.5px;">Chương Trước</span><span style="font-size: 0.95rem; font-weight: bold;">Chương {chapter_idx}: {prev_title}</span></span></a>''')
    
    # Next link
    if next_slug:
        next_title = vi_chapters[chapter_idx+1][1]
        margin_left = "margin-left: auto;" if prev_slug else ""
        nav_parts.append(f'''<a href="../{next_slug}/" class="md-footer__link" style="display: inline-flex; align-items: center; text-decoration: none; color: white; background: #2e7d32; font-weight: 500; padding: 0.6rem 1.2rem; border-radius: 6px; {margin_left}"><span style="display: flex; flex-direction: column; text-align: right;"><span style="font-size: 0.7rem; text-transform: uppercase; color: #e8f5e9; letter-spacing: 0.5px;">Chương Tiếp</span><span style="font-size: 0.95rem; font-weight: bold;">Chương {chapter_idx+2}: {next_title}</span></span><span style="font-size: 1.2rem; margin-left: 0.5rem; font-weight: bold;">→</span></a>''')
    
    nav_html = '<nav class="md-footer__inner md-grid" aria-label="Điều Hướng Chương" style="margin-top: 2.5rem; padding-top: 1.5rem; border-top: 2px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">' + ''.join(nav_parts) + '</nav>'
    return nav_html

def update_chapter_file(chapter_idx, slug):
    """Update a single Vietnamese chapter file with Prev/Next navigation."""
    filepath = os.path.join(base_path, slug, "index.html")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if navigation already exists
    if 'aria-label="Điều Hướng Chương"' in content:
        print(f"  Skipping {slug} - already has navigation")
        return False
    
    nav_html = generate_nav_html(chapter_idx)
    
    # The Vietnamese chapters don't have proper closing tags
    # Find the last substantial content and add nav before the end
    # Look for the last </p> or </h2> or similar, or just insert before the end of file
    # Let's insert before the last few empty lines
    
    # Find a good insertion point - after the last heading or paragraph
    # Look for the pattern of content ending
    lines = content.split('\n')
    
    # Find the last non-empty line with actual content
    last_content_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line and not line.startswith('<') and len(line) > 10:
            last_content_idx = i
            break
    
    if last_content_idx == -1:
        # Fallback: find last </p> or </h2>
        for i in range(len(lines) - 1, -1, -1):
            if '</p>' in lines[i] or '</h2>' in lines[i] or '</h1>' in lines[i]:
                last_content_idx = i
                break
    
    if last_content_idx == -1:
        # Last resort: insert before the end
        insert_idx = len(lines) - 3  # Before the last few empty lines
    else:
        insert_idx = last_content_idx + 1
    
    # Build new content
    new_lines = lines[:insert_idx] + ['', nav_html, ''] + lines[insert_idx:]
    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Updated {slug}")
    return True

# Process all chapters
updated = 0
for i, (slug, title) in enumerate(vi_chapters):
    print(f"Processing Chapter {i+1}: {title} ({slug})...")
    if update_chapter_file(i, slug):
        updated += 1

print(f"\nDone! Updated {updated} chapters.")