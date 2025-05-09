import os
import subprocess
import sys

def check_pip_installed():
    """检查pip是否已安装"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"检查pip时出错: {str(e)}")
        return False

def install_pip():
    """安装pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'ensurepip', '--upgrade'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        return True
    except Exception as e:
        print(f"安装pip失败: {str(e)}")
        return False

def install_requirements():
    """安装requirements.txt中的依赖"""
    try:
        if not os.path.exists('requirements.txt'):
            print("未找到requirements.txt文件")
            return False
            
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True
    except subprocess.CalledProcessError:
        print("安装依赖失败，请检查网络连接或依赖包名称")
        return False
    except Exception as e:
        print(f"安装依赖时出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 开始安装项目依赖 ===")
    
    # 检查并安装pip
    if not check_pip_installed():
        print("未检测到pip，正在安装...")
        if not install_pip():
            print("pip安装失败，请手动安装pip后重试")
            sys.exit(1)
    
    # 安装项目依赖
    print("正在安装项目依赖...")
    if install_requirements():
        print("\n=== 依赖安装完成 ===")
    else:
        print("\n=== 依赖安装失败 ===")
        sys.exit(1)