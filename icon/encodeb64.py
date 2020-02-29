import os, base64, json;


if __name__ == '__main__':
    pngName = "pytoolsip.ico";
    if os.path.exists(pngName):
        with open(pngName, 'rb') as f:
            b64Data = base64.b64encode(f.read());
        fileName = pngName.replace(".", "_")+".b64";
        with open(fileName, "w", encoding = "utf-8") as f:
            f.write(b64Data.decode());
        print(f"Base64 output file[{fileName}] success.");
    else:
        print(f"file[{fileName}] not exists!");