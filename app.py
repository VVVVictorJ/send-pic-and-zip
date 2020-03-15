from flask import Flask,url_for,request,escape,jsonify 
from werkzeug.utils import secure_filename
import os
import base64
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    #输入参数可以带有路径标识符
    return 'Subpath %s' % escape(subpath)

@app.route('/receive',methods=['POST'])
def receive():
    #测试接受base64编码过的图片
    user_id = request.form['username']
    img_filename = request.form['filename']
    test_image = base64.b64decode(request.form['b64']) #本质就是解码字符串
    upload_image_dir = "user_image"

    if not os.path.isdir(upload_image_dir) :
        os.mkdir(upload_image_dir)
    user_dir = os.path.join(upload_image_dir,user_id)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    file_path = os.path.join(user_dir,img_filename)

    #写入文件
    try:
        with open(file_path,"wb") as f:
            f.write(test_image)
            return "true"
    except:
        return "error"

@app.route('/rzip',methods=['POST'])
def zip_receive():
    zip_file = request.files.get("file")
    print("file name is {}".format(zip_file.filename))
    upload_video_dir = "upload_video_dir"
    if not os.path.isdir(upload_video_dir):
        os.mkdir(upload_video_dir)
    file_path = os.path.join(upload_video_dir,zip_file.filename)
    try:
        zip_file.save(file_path)
    except:
        return jsonify({
            zip_file.filename:"upload failed"
            })



    return jsonify({
        zip_file.filename:"done"
        })


if __name__=="__main__":
    app.run(port = 5000,debug = True)


