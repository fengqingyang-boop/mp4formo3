#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP4视频转音频工具
使用 moviepy 库提取视频中的音频
"""

import sys
import os


def install_moviepy():
    """尝试安装 moviepy 库"""
    import subprocess
    print("正在安装 moviepy 库...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
        print("moviepy 安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装 moviepy 失败: {e}")
        return False


def check_dependencies():
    """检查并安装依赖库"""
    try:
        try:
            from moviepy import VideoFileClip
            return True
        except ImportError:
            from moviepy.editor import VideoFileClip
            return True
    except ImportError:
        print("moviepy 库未安装")
        response = input("是否现在安装？(y/n): ").strip().lower()
        if response == 'y':
            return install_moviepy()
        else:
            print("请先安装 moviepy: pip install moviepy")
            return False


def import_video_file_clip():
    """导入 VideoFileClip，兼容新旧版本 moviepy"""
    try:
        from moviepy import VideoFileClip
        return VideoFileClip
    except ImportError:
        from moviepy.editor import VideoFileClip
        return VideoFileClip


def convert_mp4_to_audio(input_file, output_file=None, audio_format='mp3'):
    """
    将MP4视频转换为音频
    
    参数:
        input_file: 输入的MP4文件路径
        output_file: 输出的音频文件路径（可选）
        audio_format: 音频格式，默认 mp3
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"找不到文件: {input_file}")
        
        if not input_file.lower().endswith('.mp4'):
            raise ValueError(f"输入文件必须是MP4格式: {input_file}")
        
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.{audio_format}"
        
        VideoFileClip = import_video_file_clip()
        
        print(f"正在处理视频: {input_file}")
        print(f"输出音频: {output_file}")
        
        video = VideoFileClip(input_file)
        audio = video.audio
        
        if audio is None:
            raise ValueError("视频中没有音频轨道")
        
        audio.write_audiofile(output_file)
        
        video.close()
        audio.close()
        
        print(f"\n转换成功！音频已保存到: {output_file}")
        return True
        
    except FileNotFoundError as e:
        print(f"\n错误: {e}")
        return False
    except ValueError as e:
        print(f"\n错误: {e}")
        return False
    except ImportError as e:
        print(f"\n错误: 缺少必要的库 - {e}")
        print("请确保已安装 moviepy: pip install moviepy")
        return False
    except Exception as e:
        print(f"\n发生未知错误:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        import traceback
        print(f"\n详细错误堆栈:")
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("MP4 视频转音频工具")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print(f"  python {sys.argv[0]} <输入MP4文件> [输出音频文件]")
        print("\n示例:")
        print(f"  python {sys.argv[0]} video.mp4")
        print(f"  python {sys.argv[0]} video.mp4 audio.mp3")
        print(f"  python {sys.argv[0]} video.mp4 output.wav")
        
        input_file = input("\n请输入MP4文件路径: ").strip()
        if not input_file:
            print("未输入文件路径，程序退出。")
            sys.exit(0)
        
        output_file = input("请输入输出音频文件路径（直接回车使用默认）: ").strip()
        if output_file == '':
            output_file = None
        
        convert_mp4_to_audio(input_file, output_file)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        convert_mp4_to_audio(input_file, output_file)


if __name__ == "__main__":
    main()
