import PySimpleGUI as sg
import os

# 获取所有正在运行的进程
def get_processes():
    processes = os.popen('tasklist').readlines()
    # 创建一个列表，其中包含所有正在运行的进程名称
    process_list = [process.split()[0] for process in processes[3:]]
    return process_list

# 创建GUI窗口
layout = [[sg.Listbox(values=get_processes(), size=(40, 20), key='-LIST-')],
          [sg.Button('结束进程'), sg.Button('重启资源管理器')],
          [sg.Text('请输入要结束的进程名称（多个请用逗号或空格分隔）：')],
          [sg.InputText(key='-INPUT-'), sg.Button('批量结束')], # 添加输入框和按钮
          [sg.Button('从文件结束')] # 添加从文件结束按钮
          ]

window = sg.Window('进程杀死工具', layout)

# 进入事件循环
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == '结束进程':
        # 获取用户选择的进程名称
        selected_process = values['-LIST-'][0]
        # 结束进程
        os.system(f'taskkill /f /t /im {selected_process}')
        # 刷新列表框
        window['-LIST-'].update(get_processes())
    elif event == '重启资源管理器':
        # 结束资源管理器
        os.system('taskkill /f /im explorer.exe')
        # 重新启动资源管理器
        os.system('explorer.exe')
    elif event == '批量结束': # 添加批量结束事件
        # 获取用户输入的进程名称
        input_process = values['-INPUT-']
        # 使用逗号或空格分隔多个进程名称
        input_process_list = input_process.replace(',', ' ').split()
        # 遍历每个进程名称，并结束它们
        for process in input_process_list:
            os.system(f'taskkill /f /t /im {process}')
        # 刷新列表框
        window['-LIST-'].update(get_processes())
    elif event == '从文件结束': # 添加从文件结束事件
        # 打开 processes.txt 文件，并读取每一行内容到一个列表中
        f = open("processes.txt", "r", encoding="utf-8") # 使用 utf-8 编码
        processes = f.readlines()
        f.close()
        # 遍历这个列表，对每个进程名称进行处理，并结束对应的进程
        for process in processes:
            process = process.strip()
            os.system(f"taskkill /f /t /im {process}")
        # 刷新列表框
        window['-LIST-'].update(get_processes())

window.close()
