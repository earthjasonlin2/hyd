import os
import datetime

def human_readable_size(size):
    """Convert a size in bytes to a more human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def create_index_html(path):
    index_path = os.path.join(path, 'index.html')
    current_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    with open(index_path, 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n<meta charset="UTF-8">\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('<title>Index of ' + path.replace('\\', '/') + '</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; font-size: 16px; }\n')
        f.write('h1 { color: #333; }\n')
        f.write('ul { list-style-type: none; padding: 0; }\n')
        f.write('li { margin: 5px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px; background-color: #fff; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }\n')
        f.write('li:hover { background-color: #f0f0f0; }\n')
        f.write('a { text-decoration: none; color: inherit; display: block; width: 100%; height: 100%; }\n')
        f.write('.badge { background-color: #a0a0a0; color: #fff; padding: 3px 10px; border-radius: 12px; font-size: 12px; white-space: nowrap; }\n')
        f.write('.footer { margin-top: 20px; font-size: 14px; color: #666; text-align: center; }\n')
        f.write('.container { max-width: 800px; margin: 0 auto; padding: 20px; background-color: #fff; border: 1px solid #ddd; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        f.write('<div class="container">\n')
        f.write('<h1>Index of ' + path.replace('\\', '/') + '</h1>\n')
        f.write('<ul>\n')
        f.write('<li><a href="..">..</a></li>\n')
        html_path = ""
        html_file = ""
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if item not in ['.git', '.venv', '.github', 'index.html'] and '.log' not in item and '.py' not in item:
                if os.path.isdir(item_path):
                    html_path += f'<li><a href="{item}/">{item}/</a><span class="badge">-</span></li>\n'
                else:
                    size = human_readable_size(os.path.getsize(item_path))
                    html_file += f'<li><a href="{item}">{item}</a><span class="badge">{size}</span></li>\n'
        f.write(html_path)
        f.write(html_file)
        f.write('</ul>\n')
        f.write('<div class="footer">\n')
        f.write(f'<p>Updated on: {current_time} UTC</p>\n')
        f.write('</div>\n')
        f.write('</div>\n')
        f.write('</body>\n</html>\n')

def list_dirs_and_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames]
        # print(f"Directory: {dirpath}")
        # for filename in filenames:
        #     print(f"  File: {filename}")
        create_index_html(dirpath)

if __name__ == "__main__":
    # current_directory = os.getcwd()
    current_directory = '.'
    list_dirs_and_files(current_directory)
