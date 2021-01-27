import timg, hashlib, piexif, random, string, base64 # hashlib
from werkzeug.utils import secure_filename
from flask import send_from_directory

# viewable pages
@timg.app.route("/")
def index():
    return timg.render_template('index.html')

@timg.app.route("/u")
def upload():
    return timg.render_template('upload.html')

#@timg.app.route("/v/<file_base>/<file_name>")
#def view_image_before(file_base, file_name):
@timg.app.route("/v/<file_name>")
def view_image_before(file_name):
    file_name = secure_filename(file_name)
    image_url = ""

    upload_folder = timg.app.static_folder + "/data/uploads/"

    if not timg.os.path.isfile(upload_folder+file_name):
        return timg.redirect('/')
    else:
        image_url = '/i/' + file_name
        #image_url = '/i/' + file_base + '/' + file_name

    return timg.render_template('confirm.html', image_url=image_url)

#@timg.app.route("/i/<file_base>/<file_name>")
#def view_image(file_base, file_name):
@timg.app.route("/i/<file_name>")
def view_image(file_name):
    file_name = secure_filename(file_name)
    #file_base = file_base

    upload_folder = timg.app.static_folder + "/data/uploads/"

    if not timg.os.path.isfile(upload_folder+file_name):
        return timg.redirect('/')

    with open(upload_folder+file_name, "rb") as image_file:
        full_string = base64.b64encode(image_file.read()).decode("utf-8") # [16:]
        #encoded_string = base64.b64encode(image_file.read()).decode("utf-8")[0:16]
        
        #hashname = hashlib.sha256(encoded_string.encode()).hexdigest()[-8:]
        
    time = file_name.split('.')[0]

    #if hashname is not file_base:
    #   return timg.redirect('/')

    timg.os.system("shred -u "+upload_folder+file_name)

    return timg.render_template('view.html', img_data=full_string, timer=time)
 

# functions
@timg.app.route("/d", methods=['GET', 'POST'])
def do_upload():
    if timg.request.method == 'POST':
        timer = int(timg.request.form['timer']) if 'timer' in timg.request.form else 0
        timer_code = "0"
        encoded_string = ""

        allowed_times = [1, 5, 10, 0]
        exif_types = [".jpg", ".jpeg", ".jpe"]
        other_image_types = [".png", ".bmp", ".webp", ".gif"]

        upload_folder = timg.app.static_folder + "/data/uploads/"
        if not timg.os.path.exists(upload_folder):
            timg.os.makedirs(upload_folder)

        if timer not in allowed_times:
            timg.flash('invalid timer setting.', 'danger')
            return timg.redirect('/u')
        else:
            timer_code = str(timer)
        if 'file' not in timg.request.files:
            timg.flash('no image selected.', 'danger')
            return timg.redirect('/u')
        file = timg.request.files['file']
        if file.filename == '':
            timg.flash('no image selected.', 'danger')
            return timg.redirect('/u')
        if file:
            file_name = secure_filename(file.filename)
            extension = timg.os.path.splitext(file_name)[1]
            new_name = ''.join(random.sample("-_"+string.ascii_uppercase+string.ascii_lowercase+string.digits,20)) + extension
            new_name = timer_code + '.' + new_name
            file.save(timg.os.path.join(upload_folder, new_name))
            #with open(upload_folder+new_name, "rb") as image_file:
            #    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")[0:16]
            #    hashname = hashlib.sha256(encoded_string.encode()).hexdigest()[-8:]
            if extension in exif_types:
                piexif.remove(upload_folder + new_name)
                #timg.flash('link: <a href="/v/'+hashname+'/'+new_name+'#'+encoded_string+'">/v/'+hashname+'/'+new_name+'#'+encoded_string+'</a> (will self-destruct upon visiting)', 'success')
                timg.flash('link: <a href="/v/'+new_name+'">/v/'+new_name+'</a> (will self-destruct upon visiting)', 'success')
                return timg.redirect('/u')
            elif extension in other_image_types:
                #timg.flash('link: <a href="/v/'+hashname+'/'+new_name+'#'+encoded_string+'">/v/'+hashname+'/'+new_name+'#'+encoded_string+'</a> (will self-destruct upon visiting)', 'success')
                timg.flash('link: <a href="/v/'+new_name+'">/v/'+new_name+'</a> (will self-destruct upon visiting)', 'success')
                return timg.redirect('/u')
            else:
                timg.flash('invalid image type.', 'danger')
                timg.os.system("shred -u "+upload_folder + new_name)
                return timg.redirect('/u')
        else:
            timg.flash('invalid image.', 'danger')
            return timg.redirect('/u')
    timg.flash('no image selected.', 'danger')
    return timg.redirect('/u')


@timg.app.route("/p")
def do_purge():
    return timg.render_template('upload.html')


# internals
@timg.app.route('/robots.txt')
def robotstxt():
    return send_from_directory(timg.app.static_folder, timg.request.path[1:])

@timg.app.route('/favicon.ico')
def faviconico():
    return send_from_directory(timg.app.static_folder, timg.request.path[1:])
