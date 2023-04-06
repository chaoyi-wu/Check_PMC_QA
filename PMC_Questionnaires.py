# 读取.docx文件
# 需要使用第三方库python-docx
# 可以使用pip install python-docx安装
import os
import random
from PIL import Image
import numpy as np
import tkinter as tk
import json
from PIL import ImageTk, Image
    
# 创建窗口
window = tk.Tk()
window.title("Questionnaire")
window.geometry("512x830")
window.wm_resizable(False,True)

child_window = tk.Toplevel(window)

# Set the title of the child window
child_window.title("ChoiceBar")

# Set the size of the child window
child_window.geometry("400x160")
child_window.wm_resizable(False,False)
# 获取当前目录
current_dir = os.getcwd()

# 获取当前目录下所有文件
files = os.listdir(os.path.join(current_dir,'texts'))

# 筛选出所有.docx文件
docx_files = [f for f in files if f.endswith('.txt')]

# 构造所有.docx文件的路径
#docx_paths = [os.path.join(current_dir, f) for f in docx_files]

# 从docx_paths中随机抽取10个文件
random_files = random.sample(docx_files, 10)
ranking = {random_files[i]: -1 for i in range(len(random_files))}
var = tk.StringVar()
global point
point = 0
# 定义显示文件的函数

def save_and_close():
    ccc = 0
    while os.path.exists('rank_'+str(ccc)+'.json'):
        ccc = ccc +1
    with open('rank_'+str(ccc)+'.json', 'w') as f:
        json.dump(ranking, f)
    window.destroy()
    
def show_file():
    global point
    # 从random_files中取出第一个文件
    file_path = random_files[point]
    # 打开文件
    docx_path = os.path.join(current_dir,'texts')
    figure_path = os.path.join(current_dir,'figures')
    # Load image
    img = Image.open(os.path.join(figure_path, file_path.replace('.txt','.png')))
    img_tk = ImageTk.PhotoImage(img)
    image_label.configure(image=img_tk)
    image_label.image = img_tk
    #f = open(os.path.join(docx_path, file_path),'r')
    with open(os.path.join(docx_path, file_path),'r',encoding='utf-8') as f:
        content = f.read()
    #f.close()
    # 在窗口中显示文件内容
    text.delete('1.0', tk.END) # 清屏
    text.insert(tk.END, content)

def set_var():
    global point,var 
    if ranking[random_files[point]] != -1:
        var.set(ranking[random_files[point]])
    else:
        var.set(0)
        pass
# 定义next按钮的回调函数
def next_file():
    global point
    # 显示文件
    point = point+1
    if point <len(random_files):
        set_var()
        show_file()
    else:
       point = len(random_files)
       #text.insert(tk.END, "No more files!") 

# 定义back按钮的回调函数
def back_file():
    global point
    point = point-1
    # 如果random_files不为空
    if point>=0:
        # 显示文件
        set_var()
        show_file()
    else:
        point = 0
        #text.insert(tk.END, "The first Files!")


def print_selection():
    global point
    ranking[random_files[point]] = var.get()
    



# 创建文本框
image_label = tk.Label(window)
image_label.pack(anchor=tk.W)
text = tk.Text(window)
text.pack(anchor=tk.W)

r1 = tk.Radiobutton(child_window, text='The question is meaningful and the answer is correct.', variable=var, value='The question is meaningful and the answer is correct.', command=print_selection)
r2 = tk.Radiobutton(child_window, text='The question is meaningful but the answer is wrong.', variable=var, value='The question is meaningful but the answer is wrong.', command=print_selection)
r3 = tk.Radiobutton(child_window, text='The question is not related to images.', variable=var, value='The question is not related to images.', command=print_selection)
r4 = tk.Radiobutton(child_window, text='I cannot judge the question and the answer.', variable=var, value='I cannot judge the question and the answer.', command=print_selection)
r1.pack(side=tk.TOP, anchor=tk.W, padx=2, pady=4)
r2.pack(side=tk.TOP, anchor=tk.W, padx=2, pady=4)
r3.pack(side=tk.TOP, anchor=tk.W, padx=2, pady=4)
r4.pack(side=tk.TOP, anchor=tk.W, padx=2, pady=4)

# 创建next按钮
next_button = tk.Button(child_window, text="Next", command=next_file)
back_button = tk.Button(child_window, text="Back", command=back_file)
back_button.pack(side=tk.LEFT,anchor=tk.N) # 将back按钮放在左边
next_button.pack(side=tk.RIGHT,anchor=tk.N) # 将back按钮放在左边

finish_button = tk.Button(child_window, text='Finish', command=save_and_close)
finish_button.pack(anchor=tk.N)

# 显示第一个文件
show_file()
var.set(0)
# 进入消息循环
window.mainloop()
