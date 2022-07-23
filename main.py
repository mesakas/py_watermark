from PIL import Image
import tkinter
import os
import tkinter.filedialog
import tkinter.ttk
import tkinter.messagebox
import threading

if __name__ == '__main__':

    if not os.path.exists("./output"):
        os.mkdir("./output")

    # 图形界面
    root = tkinter.Tk()
    root.title('水印添加工具')
    root.geometry("550x190")
    # root.iconbitmap(os.path.abspath('./favicon.ico'))
    root.resizable(False, False)

    path = tkinter.StringVar()
    mark_file_path = tkinter.StringVar()

    watermark_hint = tkinter.Label(root, text="水印路径")
    watermark_hint.grid(row=0, column=0, padx=10, pady=10)

    if os.path.exists("./水印.png"):
        mark_file_path.set(os.path.abspath("./水印.png"))


    # 添加水印
    def attach_watermark(target_path):
        image = Image.open(target_path).convert("RGBA")
        watermark = Image.open(mark_file_path.get()).convert("RGBA")
        image.paste(watermark, (0, 0), watermark)
        image.save(os.path.abspath(os.path.join("./output", os.path.basename(target_path))))


    def get_file():
        val = tkinter.filedialog.askopenfilename()
        if val != "":
            mark_file_path.set(val)


    select_mark_path_button = tkinter.Button(root, text="选择水印图片", command=get_file)
    select_mark_path_button.grid(row=0, column=2, padx=10, pady=10)

    select_mark_path_Entry = tkinter.Entry(textvariable=mark_file_path, width=50)
    select_mark_path_Entry.grid(row=0, column=1)

    hint = tkinter.Label(root, text="路径")
    hint.grid(row=1, column=0, padx=10)


    def get_path():
        val = tkinter.filedialog.askdirectory()
        if val != "":
            path.set(val)


    input_entry = tkinter.Entry(root, width=50, textvariable=path)
    input_entry.grid(row=1, column=1)

    select_path_button = tkinter.Button(root, text="选择路径", command=get_path)
    select_path_button.grid(row=1, column=2, padx=10)

    progress = tkinter.StringVar()


    def multiply_attach_watermark():
        dir_path = path.get()
        file_names = os.listdir(dir_path)
        count = len(file_names)
        dir_count = 0
        for i in range(count):
            if os.path.isdir(os.path.abspath(os.path.join(dir_path, file_names[i]))):
                dir_count += 1
                progress.set(str(i + 1) + "/" + str(count) + "  （其中有" + str(dir_count) + "个文件夹）")
                continue

            attach_watermark(os.path.abspath(os.path.join(dir_path, file_names[i])))
            if dir_count == 0:
                progress.set(str(i + 1) + "/" + str(count))

            else:
                progress.set(str(i + 1) + "/" + str(count) + "  （其中有" + str(dir_count) + "个文件夹）")


    def maw_thread():
        if not os.path.exists(mark_file_path.get()):
            tkinter.messagebox.showerror("水印图片路径错误", "水印图片路径错误，请选择正确的路径")
            return

        if not os.path.exists(path.get()):
            tkinter.messagebox.showerror("图片文件夹路径错误", "图片文件夹路径错误，请选择正确的路径")
            return
        t1 = threading.Thread(target=multiply_attach_watermark)
        t1.start()


    play_button = tkinter.Button(root, text="开始添加水印", command=maw_thread)
    play_button.grid(row=2, column=2, pady=10)

    progress_label = tkinter.Label(root, textvariable=progress)
    progress.set("0/0")
    progress_label.grid(row=2, column=1, pady=10)


    def open_dir():
        if not os.path.exists(os.path.abspath("./output")):
            os.mkdir(os.path.abspath("./output"))
        os.startfile(os.path.abspath(os.path.abspath("./output")))


    open_output_dir_button = tkinter.ttk.Button(root, text="打开输出文件夹", command=open_dir, width=30)
    open_output_dir_button.grid(row=3, column=1, pady=10)

    root.mainloop()
