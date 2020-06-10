#!usr/bin/env python
#coding:utf-8

import json
import os
import sys
import zipfile
from xml.dom.minidom import parse
from tenk.overseaTest.FlagDao import flagProvider

# 读取需要更改的配置
def readConfig(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        ret_dic = json.load(f)
        return ret_dic

def un_zip(file_name,target):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(target):
        pass
    else:
        os.mkdir(target)
    for names in zip_file.namelist():
        zip_file.extract(names,target)
    zip_file.close()
    print("解压成功")


# 定义一个函数，递归读取absDir文件夹中所有文件，并塞进zipFile文件中。参数absDir表示文件夹的绝对路径。
def writeAllFileToZip(absDir, zipFile, zip_path):
    for f in os.listdir(absDir):
        absFile = os.path.join(absDir, f)  # 子文件的绝对路径
        if os.path.isdir(absFile):  # 判断是文件夹，继续深度读取。
            # relFile = absFile[len(os.getcwd()) + 1:]  # 改成相对路径，否则解压zip是/User/xxx开头的文件。
            # zipFile.write(relFile,absFile[len(os.getcwd()+"\\"+zip_path) + 1:])  # 在zip文件中创建文件夹
            zipFile.write(absFile, absFile[len(zip_path) + 1:])  # 在zip文件中创建文件夹
            writeAllFileToZip(absFile, zipFile, zip_path)  # 递归操作
        else:  # 判断是普通文件，直接写到zip文件中。
            # relFile = absFile[len(os.getcwd()) + 1:]  # 改成相对路径
            # zipFile.write(relFile, absFile[len(os.getcwd()+"\\"+zip_path) + 1:])
            zipFile.write(absFile, absFile[len(zip_path) + 1:])
    return

def zip(zip_path, target):
    # zipFilePath = os.path.join(sys.path[0], target)
    # 先定义zip文件绝对路径。sys.path[0]获取的是脚本所在绝对目录。
    # 因为zip文件存放在脚本同级目录，所以直接拼接得到zip文件的绝对路径。
    # zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
    # 创建空的zip文件(ZipFile类型)。参数w表示写模式。zipfile.ZIP_DEFLATE表示需要压缩，文件会变小。ZIP_STORED是单纯的复制，文件大小没变。

    # absDir = os.path.join(sys.path[0], zip_path)
    # 要压缩的文件夹绝对路径。

    # writeAllFileToZip(absDir, zipFile, zip_path)  # 开始压缩。如果当前工作目录跟脚本所在目录一样，直接运行这个函数。
    # 执行这条压缩命令前，要保证当前工作目录是脚本所在目录(absDir的父级目录)。否则会报找不到文件的错误。

    zipFile = zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED)
    writeAllFileToZip(zip_path, zipFile, zip_path)  # 开始压缩。
    print("压缩成功")

# 替换配置
def replaceConfig(config,unzip_file):
    if "AndroidManifest" in config.keys():
        ret_dic = json.loads(config["AndroidManifest"])
        replaceParams(unzip_file+"/AndroidManifest.xml",ret_dic)
        print("AndroidManifest替换成功")
    if "strings" in config.keys():
        ret_dic = json.loads(config["strings"])
        updateXML(unzip_file + "/res/values/values.xml", ret_dic)
        print("strings替换成功")

def replaceParams(file,ret_dic):
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            for key in ret_dic.keys():
                line = line.replace(key,ret_dic[key])
            f2.write(line)
            # f2.write(re.sub(old_str,new_str,line))
    os.remove(file)
    os.rename("%s.bak" % file, file)

def updateXML(file_xml,ret_dic):
    stringExist = {}
    flagDao = flagProvider(file_xml)
    for key in ret_dic.keys():
        if (flagDao.getValueByName("string", key) is not None):
            flagDao.setValueByName("string", key, ret_dic[key])
            stringExist[key] = True
            print("setvaluebyname", key, ret_dic[key])

    for key in ret_dic.keys():
        if key not in stringExist:
            print("addvaluebyname", key, ret_dic[key])
            flagDao.addTag("string", key, ret_dic[key])
    # domTree = parse(file_xml)
    # # 文档根元素
    # rootNode = domTree.documentElement
    # strings = rootNode.getElementsByTagName("string")
    # for str in strings:
    #     for key in ret_dic.keys():
    #         if str.getAttribute("name") == key:
    #             # 更新string的取值
    #             str.childNodes[0].data = ret_dic[key]
    #             stringExist[key] = True
    #             print("更新："+key+";"+ret_dic[key])

    # with open(file_xml, 'w', encoding='utf-8') as f:
    #     # 缩进 - 换行 - 编码
    #     domTree.writexml(f, addindent='  ', encoding='utf-8')

def main(sourcePath, config):
    print(os.getcwd())
    # ret_dic = readConfig("../config.txt")
    # print("config.txt", ret_dic, sep="\n")
    ret_dic = json.loads(config)
    print("config.txt", ret_dic, sep="\n")
    # un_zip("../"+sourcePath, "../oversea_file")
    (path, filename) = os.path.split(sourcePath)
    print("sourcePath", path, filename, sep="->")
    un_zip(sourcePath, os.path.join(path, "oversea_file"))
    replaceConfig(ret_dic, os.path.join(path, "oversea_file"))
    zip(os.path.join(path, "oversea_file"), os.path.join(path, "OVERSEA.aar"))

if __name__ == '__main__':
    # sourcePath = input()
    config = "{\n" + "    \"AndroidManifest\": \"{\\\"${FACEBOOK_APP_ID}\\\":\\\"123abcd\\\"}\",\n" + "    \"strings\": \"{\\\"facebook_app_id\\\":\\\"234abcd\\\",\\\"fb_login_protocol_scheme\\\":\\\"234abcd\\\"}\"\n" +"}"
    main("D:/python/AarSetting-master/tenk/OVERSEA-1.1.0_2.aar", config)