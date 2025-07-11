import tkinter as tk 
from tkinter import ttk, messagebox, filedialog, PhotoImage
from tkinter.ttk import Progressbar
import requests 
import os 
import time
import platform
import subprocess
import sys
import threading

def write_log(message, type="null"):
    log_file = "MYDOWNLOADER/data/log.log"

    if type == "null":
        pass
    elif type == "error":
        with open(log_file, "a", encoding="utf-8") as file:
            file.writelines(f"{time.strftime('%Y-%m-%d %H:%M:%S')} ERROR: {message}\n")
    elif type == "info":
        with open(log_file, "a", encoding="utf-8") as file:
            file.writelines(f"{time.strftime('%Y-%m-%d %H:%M:%S')} INFO: {message}\n")
    elif type == "warning":
        with open(log_file, "a", encoding="utf-8") as file:
            file.writelines(f"{time.strftime('%Y-%m-%d %H:%M:%S')} WARNING: {message}\n")
    else:
        pass

def open_download_progress(event=None):
    if url.get().strip() == "" or name.get().strip() == "":
        messagebox.showwarning("MyDownloader v1.0", "Lütfen URL ve dosya adını doldurun.")
        write_log("URL veya dosya adı boş bırakıldı.", type="warning")
        return
    
    url.delete(0, tk.END)
    name.delete(0, tk.END)
    
    global progress_window, progress_bar, label_percent

    progress_window = tk.Toplevel()
    progress_window.title("İndirme İlerlemesi")
    progress_window.geometry("400x100")
    progress_window.attributes("-topmost", True)

    root_x = 400
    root_y = 100

    window_x = root.winfo_screenwidth() // 2 - root_x // 2
    whindow_y = root.winfo_screenheight() // 2 - root_y // 2
    progress_window.geometry(f"{root_x}x{root_y}+{window_x}+{whindow_y}")

    progress_bar = Progressbar(progress_window, length=300, mode='determinate')
    progress_bar.pack(pady=20)

    label_percent = ttk.Label(progress_window, text="%0", font=("Century Gothic", 12, "bold"))
    label_percent.pack()

    indir_baslat()

def dosya_indir(url, hedef_dosya, progressbar, yuzde_label):
    try:
        response = requests.get(url, stream=True)
        toplam_boyut = int(response.headers.get('content-length', 0))
        indirilen = 0

        with open(hedef_dosya, "wb") as f:
            for parca in response.iter_content(8192):
                if parca:
                    f.write(parca)
                    indirilen += len(parca)
                    if toplam_boyut > 0:
                        oran = (indirilen / toplam_boyut) * 100
                        progressbar["value"] = oran
                        yuzde_label.config(text=f"%{int(oran)}")
                        root.update_idletasks()
                        progress_window.update_idletasks()

        yuzde_label.config(text="İndirme İşlemi Tamamlandı!")
        write_log(f"{os.path.basename(hedef_dosya)} başarıyla indirildi. URL : {url} - NAME : {hedef_dosya}", type="info")
        progress_bar["value"] = 100
        yuzde_label.config(text="%100")
        time.sleep(1)
        progress_window.destroy()
    except Exception as e:
        yuzde_label.config(text="Hata!")
        write_log(str(e), type="error")
        messagebox.showerror("MyDownloader v1.0 Error MSG", f"İndirme sırasında bir hata oluştu: {str(e)}")

def indir_baslat():
    url_v = url.get().strip()
    if not url_v:
        return

    dosya_adi = os.path.basename(url_v)
    kaydet_yolu = filedialog.asksaveasfilename(initialfile=dosya_adi)

    if kaydet_yolu:
        progress_bar["value"] = 0
        label_percent.config(text="%0")
        threading.Thread(
            target=dosya_indir,
            args=(url_v, kaydet_yolu, progress_bar, label_percent),
            daemon=True
        ).start()

def about():
    about_file = "MYDOWNLOADER/info/about.txt"
    os.startfile(os.path.abspath(about_file))

def helper():
    helper_file = "MYDOWNLOADER/info/helper.txt"
    os.startfile(os.path.abspath(helper_file))

def open_log():
    log_file = "MYDOWNLOADER/data/log.log"
    os.startfile(os.path.abspath(log_file))

def main():
    global url, name, root

    try:
        about_text = "Bu uygulama internetten URL girdiğiniz dosyayı indirir. Şu anda DEMO aşamasında olan\nuygulama geliştirilmeye devam edilecektir.\n\nYayıncı : TheKeops\nGeliştirici : TheKeops\nLisans : MIT LICENSE\nVersiyon : v1.0"
        helper_text = "Dosya URL yazan yere dosyanın url adresini giriniz, dosya adı yazan yere ise\nkayıt olacak dosya adını giriniz. Ardından 'İndir' butonuna basın.\n\nEğer hata alırsanız URL adresi yanlış girilmiş olabilir veya URL adresi\ngeçersiz olmuş olabilir."

        os.makedirs("MYDOWNLOADER", exist_ok=True)
        os.makedirs("MYDOWNLOADER/data", exist_ok=True)
        os.makedirs("MYDOWNLOADER/info", exist_ok=True)
        open("MYDOWNLOADER/data/appdata.txt", "x", encoding="utf-8").write("false")
        open("MYDOWNLOADER/data/log.log", "x", encoding="utf-8")

        open("MYDOWNLOADER/info/about.txt", "x", encoding="utf-8").write(about_text)
        open("MYDOWNLOADER/info/helper.txt", "x", encoding="utf-8").write(helper_text)
    except FileExistsError:
        pass

    write_log("MyDownloader v1.0 uygulaması açıldı.", type="info")

    root = tk.Tk()
    root.title("MyDownloader v1.0")
    root.resizable(False, False)
    path_find = os.path.abspath("MYDOWNLOADER/assets/icons/MyDownloaderLogo.png")
    path_find = path_find.replace("\\", "/")
    the_icon = PhotoImage(file=path_find)
    root.iconphoto(True, the_icon)

    root_x = 500
    root_y = 300

    window_x = root.winfo_screenwidth() // 2 - root_x // 2
    whindow_y = root.winfo_screenheight() // 2 - root_y // 2
    root.geometry(f"{root_x}x{root_y}+{window_x}+{whindow_y}")

    os_platform = platform.system()

    title = tk.Label(root, text="MyDownloader v1.0", font=("Century Gothic", 16,"bold"))
    title.pack(pady=10)

    url_title = tk.Label(root,fg="red" ,text="Dosya URL:", font=("Century Gothic", 12,"bold"))
    url_title.pack(pady=5)

    url = ttk.Entry(root, width=50, font=("Century Gothic", 12, "bold"))
    url.pack(pady=5)

    name_title = tk.Label(root,fg="red" ,text="Dosya Adı:", font=("Century Gothic", 12,"bold"))
    name_title.pack(pady=5)

    name = ttk.Entry(root, width=50, font=("Century Gothic", 12, "bold"), justify="center")
    name.pack(pady=5)

    start_button = ttk.Button(root, text="İndir", command=open_download_progress)
    start_button.pack(pady=10)
    start_button.bind("<Return>", open_download_progress)

    menu = tk.Menu(root)
    root.config(menu=menu)
    menu_app = tk.Menu(menu, tearoff=0)
    menu_app.add_command(label="Hakkında", command=about)
    menu_app.add_command(label="Yardım", command=helper)
    menu_app.add_command(label="Log Dosyası", command=open_log)
    menu_app.add_separator()
    menu_app.add_command(label="Çıkış", command=root.quit)

    menu.add_cascade(label="Menu", menu=menu_app)

    root.bind("<Control-q>", lambda e: root.quit())
    root.bind("<Control-Q>", lambda e: root.quit())
    root.bind("<Return>", open_download_progress)
    root.bind("<Escape>", lambda e: root.quit())
    root.bind("<F1>", lambda e: messagebox.showinfo("MyDownloader v1.0", f"URL : {url.get()}\nDosya Adı : {name.get()}"))

    if os_platform == "Windows":    
        with open("MYDOWNLOADER/data/appdata.txt", "r") as data_file:
            data = data_file.read().strip().lower()

            if data == "true":
                start_button.config(state="normal")
            elif data == "false":
                start_button.config(state="disabled")
                messagebox.showinfo("MyDownloader v1.0","Uygulamanın çalışabilmesi için 'requests' modülünün yüklenmesi gerekiyor. Uygulama otomatik olarak yükleyecektir ve otomatik kapatılacaktır.")
                write_log("Requests modülü yükleniyor...", type="info")
                subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "requests"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
    )
                with open("MYDOWNLOADER/data/appdata.txt", "w") as data_file:
                    data_file.write("true")
                messagebox.showinfo("MyDownloader v1.0", "Modül indirme işlemi başarılı! Lütfen uygulamayı tekrar başlatın.")
                write_log("Requests modülü başarıyla yüklendi.", type="info")
                root.destroy()
            else:
                with open("MYDOWNLOADER/data/appdata.txt", "w") as data_file:
                    data_file.write("false")
                start_button.config(state="disabled")
                messagebox.showerror("MyDownloader v1.0 Error MSG", "Uygulama verisi bozuk! Lütfen uygulamayı tekrar başlatın.")
                write_log("Uygulama verisi bozuk!", type="error")
                root.destroy()
    else:
        start_button.config(state="disabled")
        messagebox.showerror("MyDownloader v1.0 Error MSG", "Bu platform desteklenmiyor! Kullandığınız platform: " + os_platform)
        write_log(f"Desteklenmeyen platform: {os_platform}", type="error")
        root.destroy()

    root.mainloop()

if __name__ == "__main__":
    main()
    write_log("MyDownloader v1.0 uygulaması kapatıldı.", type="info")
