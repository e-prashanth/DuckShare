from flask import Flask,render_template, request, jsonify , send_file
import os
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from pymongo import MongoClient


MongoURL = 'mongodb+srv://edeprashanth:Zpmr00ME8U0eqMpo@cluster0.yfyrqet.mongodb.net/'

def getClient():
    client = MongoClient(MongoURL)
    return client

app = Flask(__name__)

@app.route('/')
def HomePage():
    print(MongoURL)
    return render_template('index.html')

@app.route('/api/add-file', methods=['POST'])
def add_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file to the Upload folder
    upload_folder = 'Uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(upload_folder, filename)
    uploaded_file.save(file_path)

    # Now, you can store the file details in the database
    client = getClient()
    db = client.DuckShareDb
    files = db.Files
    # Example: Inserting file details into the database
    file_data = {
        'filename': filename,
        'path': file_path,
    }
    insert_result = files.insert_one(file_data)
    file_id = str(insert_result.inserted_id)

    # Create a new document in the 'codes' collection
    codes = db.Codes
    code_data = {
        'file_id': file_id[-10:],  # Last 7 digits of the file ID
        'fileid': ObjectId(file_id)
    }
    codes.insert_one(code_data)

    return jsonify({'success': 'File uploaded successfully', 'file_id': file_id[-10:] , 'file_name':filename})



@app.route("/file/<id>", methods=["GET"])
def getFile(id):
    client = getClient()
    db = client.DuckShareDb
    Files = db.Files
    codes = db.Codes
    code = codes.find_one({"file_id": id})  # Use find_one() to get a single document
    if code:
        File = Files.find_one({"_id":code['fileid']})
        if File:
            return jsonify({"fileName":File['filename']}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
        
    else:
        # If no matching document is found, return an error message
        return jsonify({'error': 'File not found'}), 404
    



@app.route("/download/<path:file_path>")
def download_file(file_path):
    full_file_path = os.path.join(app.root_path, file_path)
    
    if not os.path.exists(full_file_path):
        return "File not found", 404
    return send_file(full_file_path, as_attachment=True)




@app.route('/getfiles/<fileData>')
def getFiles(fileData):
    return render_template("aftercode.html",fileData['fileName'])


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)