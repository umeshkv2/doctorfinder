from flask import Flask,render_template,request,session,redirect,url_for
import pymysql,os,time
from databaselib import *
from photolib import *
from werkzeug.utils import secure_filename
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='./static/uploadphoto'
app.secret_key="session super key"
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/hospital_form',methods=['GET','POST'])
def hospital():
    if 'usertype' in session:
        email=session['email']
        if session['usertype']=='admin':
            if request.method=='POST':
                hn=request.form['v1']
                sp = request.form['v2']
                ad = request.form['v3']
                ct = request.form['v4']
                ab = request.form['v5']
                nab = request.form['v6']
                em = request.form['v7']
                ps = request.form['v8']
                cur=getdbcur()
                sql="insert into hospitaldata values('"+hn+"','"+sp+"','"+ad+"','"+ct+"','"+ab+"','"+nab+"','"+em+"')"
                sql1="insert into logindata values('"+em+"','"+ps+"','hospital');"
                n=cur.execute(sql)
                m=cur.execute(sql1)
                msg1="Error:Data can't save"
                if (n==1 and m==1):
                    print("data inserted")
                    msg1="Data successfully saved"
                    return render_template('hospital.html',hmess=msg1)
                else:
                    print("Data not inserted")
                    return render_template('hospital.html',hmess=msg1)
            else:
                return render_template('hospital.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/show_hospital')
def show_hospital():
    cur=getdbcur()
    sql="select * from hospitaldata"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        print("data is found in table")
        data=cur.fetchall()
        return render_template('showhospital.html',adata=data)
    else:
        return render_template('showhospital.html',amess="There is no data of Hospital available")
@app.route('/edit_form',methods=['GET','POST'])
def edit_form():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                em=request.form['h1']
                cur=getdbcur()
                sql="select * from hospitaldata where email='"+em+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template('editform.html',edata=data)
                else:
                    return render_template('editform.html',emsg="NO Data Found")
            else:
                return redirect(url_for('show_hospital'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/edit_details',methods=['GET','POST'])
def edit_details():
    if request.method=='POST':
        hn = request.form['v1']
        sp = request.form['v2']
        ad = request.form['v3']
        ct = request.form['v4']
        ab = request.form['v5']
        nab = request.form['v6']
        em = request.form['v7']
        sql = "update hospitaldata set hospital_name='" + hn + "',speciality='" + sp + "',address='" + ad + "',contact='" + ct + "',ac_beds='" + ab + "',non_ac_beds='" + nab + "' where email='" + em + "'"
        cur=getdbcur()
        cur.execute(sql)
        n = cur.rowcount
        if n>0:
            return render_template('editmess.html',efmsg= "Data Edited Successfully")
        else:
            return render_template('editmess.html',efmsg= "Data NOT Edited")
    else:
        return redirect(url_for('show_hospital'))
@app.route('/admin_home')
def admin_home():
    if 'usertype' in session:
        email=session['email']
        if session['usertype']=='admin':
            photo=check_upload(email)
            cur=getdbcur()
            sql="select name from admindata where email='"+email+"'"
            cur.execute(sql)
            data=cur.fetchone()
            name=data[0]
            return render_template('adminhome.html',eml=email,photo=photo,name=name)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/hospital_home')
def hospital_home():
    if 'usertype' in session:
        email=session['email']
        if session['usertype']=='hospital':
            photo = check_upload(email)
            cur = getdbcur()
            sql = "select hospital_name from hospitaldata where email='" + email + "'"
            cur.execute(sql)
            data = cur.fetchone()
            name=data[0]
            return render_template('hospitalhome.html',eml=email,photo=photo,name=name)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['v1']
        password=request.form['v2']
        cur=getdbcur()
        sql="select * from logindata where email='"+email+"' and password='"+password+"';"
        cur.execute(sql)
        n=cur.rowcount
        if n==1:
            #fetching usertype whether Admin or Hospital
            ldata=cur.fetchone()
            uty=ldata[2]
            email=ldata[0]
            session['usertype']=uty
            session['email']=email
            if session['usertype']=='admin':
                return redirect(url_for('admin_home'))
            elif session['usertype']=='hospital':
                return redirect(url_for('hospital_home'))
            elif session['usertype']=='store':
                return redirect(url_for('medicalstore_home'))
        else:
            return  render_template('login.html',lmsg="Incorrect email or password")
    else:
        return render_template('login.html')
@app.route('/change_password_admin',methods=['GET','POST'])
def change_passsword_admin():
    if 'usertype' in session:
        email=session['email']
        if session['usertype']=='admin':
            if request.method=='POST':
                oldpass=request.form['v2']
                newpass=request.form['v3']
                sql="update logindata set password='"+newpass+"' where email='"+email+"' AND password='"+oldpass+"' AND usertype='admin';"
                cur=getdbcur()
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    session.pop('usertype', None)
                    return render_template('changepasswordadmin.html',cmsg="Password changed Successfully")
                else:
                    return render_template('changepasswordadmin.html',cmsg="Incorrect Email Or Oldpassword or new password and old password is same")
            else:
                return render_template('changepasswordadmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/change_password_hospital', methods=['GET', 'POST'])
def change_passsword_hospital():
    if 'usertype' in session:
        email=session['email']
        if session['usertype'] == 'hospital':
            if request.method == 'POST':
                oldpass = request.form['v2']
                newpass = request.form['v3']
                sql = "update logindata set password='" + newpass + "' where email='" + email + "' AND password='" + oldpass + "' AND usertype='hospital';"
                cur = getdbcur()
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    session.pop('usertype', None)
                    return render_template('changepasswordhospital.html', cmsg="Password changed Successfully login again... by clicking at above")
                else:
                    return render_template('changepasswordhospital.html', cmsg="Incorrect Email Or Oldpassword Or new password and old password is same")
            else:
                return render_template('changepasswordhospital.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    if 'usertype' in session:
        uty=session['usertype']
        email=session['email']
        if request.method=='POST':
            name=request.form['v1']
            address = request.form['v2']
            contact = request.form['v3']
            cur=getdbcur()
            sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                return render_template('adminprofilemessage.html',msg="Data changes saved sucssesfully")
            else:
                return render_template('adminprofilemessage.html',msg="Data can't be changed..")
        else:
            #showing the default data beore saving
            cur=getdbcur()
            sql="select * from admindata where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data=cur.fetchone()
                return render_template('adminprofile.html',pdata=data)
            else:
                return render_template('adminprofile.html',pmsg="Data not found")
    else:
        return redirect(url_for('auth_error'))
@app.route('/doctor_registration',methods=['GET','POST'])
def doctor_registration():
    if 'usertype' in session:
        uty=session['usertype']
        email=session['email']
        if session['usertype']=='hospital':
            if request.method=='POST':
                name=request.form['v1']
                speciality=request.form['v2']
                timing=request.form['v3']
                experience=request.form['v4']
                cur=getdbcur()
                sql="insert into doctordata values('"+name+"','"+speciality+"','"+timing+"','"+experience+"','"+email+"');"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('doctorregistration.html',drmsg="Doctor registered successfully")
                else:
                    return render_template('doctorregistration.html',drmsg="Can't Registered doctor")
            else:
                return render_template('doctorregistration.html')
        else:
            return render_template('doctorregistration.html',drmsg="Admin are Not allowed to register doctor")
    else:
        return redirect(url_for('auth_error'))
@app.route('/auth_error')
def auth_error():
    return  render_template('autherror.html')
@app.route('/upload_admin_photo')
def upload_admin_photo():
    return render_template('uploadadminphoto.html')
@app.route('/upload_adminphoto_mess',methods=['GET','POST'])
def upload_adminphoto_mess():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method=='POST':
                p=request.files['p1']
                if p:
                    path=os.path.basename(p.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='hospital',autocommit=True)
                    cur=conn.cursor()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            p.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('adminphotouploadmess.html',mess="photo uploaded successfully")
                        else:
                            return render_template('adminphotouploadmess.html', mess="photo not uploaded")
                    except:
                        return render_template('adminphotouploadmess.html',mess="photo already available")
                else:
                    return render_template('adminphotouploadmess.html',mess="please select a photo to upload")
            else:
                return redirect(url_for('photo_upload_admin'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/change_admin_photo')
def change_admin_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo=check_upload(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='hospital', autocommit=True)
            cur=conn.cursor()
            sql="delete from photodata where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/uploadphoto/"+photo)
                return render_template('adminphotouploadmess.html',mess="photo deleted successfully")
            else:
                return render_template('adminphotouploadmess.html',mess="photo deletion failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/upload_hospital_photo')
def upload_hospital_photo():
    return render_template('uploadhospitalphoto.html')
@app.route('/upload_hospitalphoto_message')
def upload_hospitalphoto_message():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='hospital':
            if request.method=='POST':
                q=request.files['p1']
                if q:
                    path=os.path.basename(q.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='hospital',autocommit=True)
                    cur=conn.cursor()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            q.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('hospitalphotouploadmess.html',upmess="photo uploaded successfully")
                        else:
                            return render_template('hospitalphotouploadmess.html',upmess="photo not uploaded")
                    except:
                        return render_template('hospitalphotouploadmess.html',upmess="photo already available")
                else:
                    return render_template('hospitalphotouploadmess.html',upmess="please select a photo to upload")
            else:
                return redirect(url_for('photo_upload_hospital'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/change_hospital_photo')
def change_hospital_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='hospital':
            photo=check_upload(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='hospital', autocommit=True)
            cur=conn.cursor()
            sql="delete from photodata where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/uploadphoto/"+photo)
                return render_template('hospitalphotouploadmess.html',upmess="photo deleted successfully")
            else:
                return render_template('hospitalphotouploadmess.html',upmess="photo deletion failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    if 'usertype' in session:
        uty=session['usertype']
        if uty=='admin':
            if request.method=='POST':
                nm=request.form['v1']
                ad=request.form['v2']
                ct=request.form['v3']
                em=request.form['v4']
                pd=request.form['v5']
                cur=getdbcur()
                sql="insert into admindata values('"+nm+"','"+ad+"','"+ct+"','"+em+"')"
                sql1="insert into logindata values('"+em+"','"+pd+"','admin')"
                n=cur.execute(sql)
                m=cur.execute(sql1)
                if n==1 and m==1:
                    return render_template('adminreg.html',mess="registration successful")
                else:
                    return render_template('adminreg.html',mess="input all fileds or already register")
            else:
                return render_template('adminreg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/hospital_profile',methods=['GET','POST'])
def hospital_profile():
    if 'usertype' in session:
        uty=session['usertype']
        email=session['email']
        if request.method=='POST':
            hn = request.form['v1']
            sp = request.form['v2']
            ad = request.form['v3']
            ct = request.form['v4']
            ab = request.form['v5']
            nab = request.form['v6']
            cur=getdbcur()
            sql="update hospitaldata set hospital_name='"+hn+"',speciality='"+sp+"',address='"+ad+"',contact='"+ct+"' ,ac_beds='"+ab+"',non_ac_beds='"+nab+"' where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                return render_template('hospitalprofilemessage.html',msg="Data changes saved sucssesfully")
            else:
                return render_template('hospitalprofilemessage.html',msg="Data can't be changed..")


        else:
            #showing the default data beore saving
            cur=getdbcur()
            sql="select * from hospitaldata where email='"+email+"';"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data=cur.fetchone()
                return render_template('hospitalprofile.html',pdata=data)
            else:
                return render_template('hospitalprofile.html',pmsg="Data not found")
    else:
        return redirect(url_for('auth_error'))
@app.route('/show_doctors')
def show_doctors():
    if 'usertype' in session:
        uty=session['usertype']
        email=session['email']
        if uty=='hospital':
            cur=getdbcur()
            sql="select * from doctordata where email_of_hospital='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchone()
                return render_template('showdoctors.html',a=data)
            else:
                return render_template('showdoctors.html',mess="Doctors details not found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/show_admins')
def show_admins():
    if 'usertype' in session:
        uty = session['usertype']
        email = session['email']
        if uty == 'admin':
            cur = getdbcur()
            sql = "select * from admindata "
            cur.execute(sql)
            n = cur.rowcount
            if n>0:
                print("data is found in table")
                data = cur.fetchall()
                return render_template('showadmins.html',data=data)
            else:
                return render_template('showadmins.html',mess="There is no data available for other admins")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/medicalstore_reg',methods=['GET','POST'])
def medicalstore_reg():
    if 'usertype' in session:
        uty = session['usertype']
        if uty == 'hospital':
            if request.method == 'POST':
                nm = request.form['v1']
                ad = request.form['v2']
                ct = request.form['v3']
                em = request.form['v4']
                pd = request.form['v5']
                cur = getdbcur()
                try:
                    sql = "insert into medicalstoredata values('" + nm + "','" + ad + "','" + ct + "','" + em + "')"
                    sql1 = "insert into logindata values('" + em + "','" + pd + "','store')"
                    n = cur.execute(sql)
                    m = cur.execute(sql1)
                    if n == 1 and m == 1:
                        return render_template('medicalstorereg.html', mess="registration successful")
                    else:
                        return render_template('medicalstorereg.html', mess="input all fileds")
                except:
                    return render_template('medicalstorereg.html',mess="Medicalstore is already registered")
            else:
                return render_template('medicalstorereg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))
@app.route('/medicalstore_view')
def medicalstore_view():
    cur = getdbcur()
    sql = "select * from medicalstoredata;"
    cur.execute(sql)
    n = cur.rowcount
    if n > 0:
        data = cur.fetchall()
        return render_template('viewmedicalstore.html', mdata=data)
    else:
        return render_template('viewmedicines.html', mess="Medicial Stores details not found")
@app.route('/medicalstore_home')
def medicalstore_home():
    if 'usertype' in session:
        email=session['email']
        if session['usertype']=='store':
            photo=check_upload(email)
            cur=getdbcur()
            sql="select name from medicalstoredata where email='"+email+"'"
            cur.execute(sql)
            data=cur.fetchone()
            name=data[0]
            return render_template('medicalstorehome.html',eml=email,name=name)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medicine_reg',methods=['GET','POST'])
def medicine_reg():
    if 'usertype' in session:
        email = session['email']
        if session['usertype'] == 'store':
            if request.method == 'POST':
                name = request.form['v1']
                quantity = request.form['v2']
                price = request.form['v3']
                use = request.form['v4']
                cur = getdbcur()
                sql = "insert into medicinedata values('" + name + "','" + quantity + "','" + price + "','" + use + "','" + email + "');"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('medicinereg.html', mrmsg="Medicine registered successfully")
                else:
                    return render_template('medicinereg.html', mrmsg="Can't Registered Medicine")
            else:
                return render_template('medicinereg.html')
        else:
            return render_template('medicinereg.html', mrmsg="Admin or Hospital are Not allowed to register Medicine")
    else:
        return redirect(url_for('auth_error'))
@app.route('/view_medicines')
def view_medicines():
    cur = getdbcur()
    sql = "select * from medicinedata;"
    cur.execute(sql)
    n = cur.rowcount
    if n > 0:
        data = cur.fetchall()
        return render_template('viewmedicines.html', mdata=data)
    else:
        return render_template('viewmedicines.html', mess="Medicines details not found")
if __name__ == '__main__':
    app.run(debug=True)
