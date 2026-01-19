from flask import Flask, jsonify, render_template, redirect, request,url_for, flash
import config, func
import os
import checks
import json



#from flask_cors import CORS


app=Flask(__name__)
#CORS(app,resources={r"/api/*":{"origins":"*"}})

#setting the upload folder
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key="secret_key"


   
#file upload handler method and index route
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and func.allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("csv_preview", name=filename))

    return render_template("index.html")
#csv preview function
@app.route('/preview/<name>')
def csv_preview(name):
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    previewData=func.preview(path)

    #converts csv data to html table
    
    return render_template("index.html",file=name, table=previewData[1], dtypes=previewData[0],nrows=previewData[4],ncols=previewData[3],col_names=list(previewData[2]))

@app.route('/files', methods=['GET'])
def list_uploaded_files():
    folder = app.config['UPLOAD_FOLDER']

    try:
        files = [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]
    except FileNotFoundError:
        files = []

    return jsonify({
        "files": files,
        "count": len(files)
    })

    
@app.route('/files/<filename>', methods=['DELETE'])
def delete_uploaded_file(filename):
    folder = app.config['UPLOAD_FOLDER']
    file_path = os.path.join(folder, filename)

    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404

    os.remove(file_path)
    return jsonify({"message": f"{filename} deleted successfully"})


@app.route('/imbalance/<name>', methods=["GET","POST"])
def classImb_test(name):
    # serves the class imbalance results
    
    data = request.get_json()
    variable = data.get("var")
  
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.FairnessAudit(path,variable)

    
    res=ethic_model.check_class_imbalance()
    
    return jsonify(res)


@app.route('/demo_bias/<name>', methods=["GET","POST"])
def demo_bias(name):
    # serves the demographic bias results
    data = request.get_json()
    
    variable = data.get("var")
        
   
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.FairnessAudit(path,variable)

    res=ethic_model.demographic_bias()

    return jsonify(res)
    
@app.route('/representation/<name>', methods=["GET","POST"])
def rep_check(name):

    data = request.get_json()
    variable = data.get("var")
    
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.FairnessAudit(path,variable)

       
    res=ethic_model.check_representation()

    return jsonify(res)
    
@app.route('/correlation/<name>', methods=["GET","POST"])
def corr_check(name):
 
        
    data = request.get_json()
    variable = data.get("var")
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.FairnessAudit(path,variable)

        
    res=ethic_model.correlation_with_protected()

    return jsonify(res)





@app.route('/overfitting/<name>', methods=["GET","POST"])
def overfitting_check(name):
 

    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.algorithmic_checks(path)

    res=ethic_model.overfitting_check()

    return jsonify(res)


@app.route('/leakage/<name>', methods=["GET","POST"])
def data_leakage_check(name):

        
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.algorithmic_checks(path)

    res=ethic_model.data_leakage_check()
   
    return jsonify(res)


@app.route('/missing_values/<name>', methods=["GET","POST"])
def miss_values_check(name):
        
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.algorithmic_checks(path)

    res=ethic_model.miss_values_check()
 
    return jsonify(res)


@app.route('/outliers/<name>', methods=["GET","POST"])
def out_impact_check(name):

        
    path=os.path.join(app.config['UPLOAD_FOLDER'], name)
    ethic_model=checks.algorithmic_checks(path)

    res=ethic_model.out_impact_check()
  
    return jsonify(res)
    



if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)