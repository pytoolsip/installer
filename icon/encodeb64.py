import os, base64


if __name__ == '__main__':
    if os.path.exists("dzjh.ico"):
        with open("dzjh.ico", 'rb') as f:
            b64Data = base64.b64encode(f.read());
            print(b64Data.decode());