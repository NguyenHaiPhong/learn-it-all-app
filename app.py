import mlab
from models.classes import *
from datetime import datetime
from flask import *
from youtube_dl import YoutubeDL 
app = Flask(__name__)

mlab.connect()
app.secret_key = "lia"

#. Homepage
@app.route("/")
def homepage():
    return render_template("/page/homepage.html")

#. About us
@app.route("/about-us")
def about_us():
    return  render_template("page/about-us.html")

#. User sign in - 1
# @lia_app.route("/user/user-sign-in", defaults={"redirect_url": None}, methods = ["GET", "POST"])
# @lia_app.route("/user/user-sign-in/<redirect_url>", methods = ["GET", "POST"])
# def user_sign_in(redirect_url):
#     error = None
#     if request.method == "GET":  
#         if "admin_signed_in" in session:
#             return redirect(url_for("admin_page"))
#         elif "customer_signed_in" in session:
#             return redirect(url_for(redirect_url))
#         else:
#             return render_template("user/user-sign-in.html")
#     elif request.method == "POST":
#         form = request.form
#         sign_in = form["sign-in"]
#         password = form["password"]
#         all_users = User.objects(sign_in__exact = sign_in, 
#         password__exact = password)
#         if len(all_users) != 0: 
#                 user_id = all_users[0].id
#                 if all_users[0].is_admin:
#                     session["admin_signed_in"] = True
#                     session["admin_signed_in_id"] = str(user_id)
#                     return redirect(url_for("admin_page"))
#                 elif all_users[0].is_admin == False:
#                     session["customer_signed_in"] = True
#                     session["customer_signed_in_id"] = str(user_id)
#                     return redirect(url_for(redirect_url))
#         elif len(all_users) == 0:
#             flash("Wrong username or password")
#             error = ("Sai Tài Khoản")
#             return render_template("user/user-sign-in.html", error = error)

#. User sign in - 2
@app.route("/user-sign-in", methods = ["GET", "POST"])
def user_sign_in():
    error = None
    if request.method == "GET":  
        if "admin_signed_in" in session:
            return redirect(url_for("admin_page"))
        elif "customer_signed_in" in session:
            return redirect(url_for("customer_profile"))
        else:
            return render_template("user/user-sign-in.html")
    elif request.method == "POST":
        form = request.form
        sign_in = form["sign-in"]
        password = form["password"]
        all_users = User.objects(sign_in__exact = sign_in, 
        password__exact = password)
        if len(all_users) != 0: 
                user_id = all_users[0].id
                if all_users[0].is_admin:
                    session["admin_signed_in"] = True
                    session["admin_signed_in_id"] = str(user_id)
                    return redirect(url_for("admin_page"))
                elif all_users[0].is_admin == False:
                    session["customer_signed_in"] = True
                    session["customer_signed_in_id"] = str(user_id)
                    return redirect(url_for("homepage"))
        elif len(all_users) == 0:
            flash("Wrong username or password")
            error = ("Sai Tài Khoản")
            return render_template("user/user-sign-in.html", error = error)

# ---ADMIN---
#. Admin page
@app.route("/admin")
def admin_page():
    if "admin_signed_in" in session:
        return render_template("user/admin/admin.html")
    else:
        return redirect(url_for("user_sign_in"))

#. Show all lecturers
@app.route("/admin/show-all-lecturers")
def admin_show_all_lecturers():
    if "admin_signed_in" in session:
        all_lecturers = Lecturer.objects()
        return render_template("user/admin/show-all-lecturers.html", 
        all_lecturers = all_lecturers)
    else:
        return redirect(url_for("user_sign_in"))

#. Show all customers
@app.route("/admin/show-all-customers")
def admin_show_all_customers():
    if "admin_signed_in" in session:
        all_customers = User.objects(is_admin = False)
        return render_template("user/admin/show-all-customers.html", 
        all_customers = all_customers)
    else:
        return redirect(url_for("user_sign_in"))

#. Show all orders
@app.route("/admin/show-all-orders")
def admin_show_all_orders():
    if "admin_signed_in" in session:
        all_orders = Order.objects()
        return render_template("user/admin/show-all-orders.html", 
        all_orders = all_orders)
    else:   
        return redirect(url_for("user_sign_in"))

#Show all courses
@app.route("/admin/show-all-courses")
def admin_show_all_courses():
    if "admin_signed_in" in session:
        all_courses = Course.objects()
        return render_template("user/admin/show-all-courses.html", 
            all_courses = all_courses)
    else:
        return redirect(url_for("user_sign_in"))

#. Update lecturer
@app.route("/admin/update-lecturer/<lecturer_id>", methods = ["GET", "POST"])
def admin_update_lecturer(lecturer_id):
    lecturer = Lecturer.objects.with_id(lecturer_id)
    if request.method == "GET":
        if "admin_signed_in" in session:
            return render_template("user/admin/update-lecturer.html", lecturer = lecturer)
        else:
            return redirect(url_for("user_sign_in"))
    elif request.method == "POST":
        form = request.form     
        name = form["name"]
        email = form["email"]
        height = form["height"]
        weight = form["weight"]
        phone_number = form["phone-number"]
        body_fat = form["body-fat"]
        description = form["description"]
        lecturer.update(set__name = name, set__email = email,
        set__height = height, set__weight = weight,set__body_fat = body_fat, set__phone_number = phone_number, 
        set__description = description)
        Lecturer.reload(lecturer)
        return redirect(url_for("admin_show_all_lecturers"))

#. Update course
@app.route("/admin/update-course/<course_id>", methods = ["GET", "POST"])
def admin_update_course(course_id):
    course = Course.objects.with_id(course_id)
    if request.method == "GET":
        if "admin_signed_in" in session:   
            return render_template("user/admin/update-course.html", course = course)
        else:
            return redirect(url_for("user_sign_in"))
    elif request.method == "POST":
        form = request.form     
        name = form["name"]
        level = form["level"]
        fee = form["fee"]
        description = form["description"]
        course.update(set__name = name, set__level = level,
        set__fee = fee, set__description = description)
        Course.reload(course)
        return redirect(url_for("admin_show_all_courses"))

#. Accept Order
@app.route("/admin/accept-order/<order_id>")
def admin_accept_orders(order_id):
    if "admin_signed_in" in session:
        order = Order.objects.with_id(order_id)
        order.update(set__is_purchased = True)
        Order.reload(order)
        return redirect(url_for("admin_show_all_orders"))            
    else:   
        return redirect(url_for("user_sign_in"))

#. Delete Lecturer
@app.route("/admin/del-lecturer/<lecturer_id>")
def admin_del_lecturer(lecturer_id):
    lecturer = Lecturer.objects.with_id(lecturer_id)
    if "admin_signed_in" in session:
        lecturer.update(set__is_activating = False)
        Lecturer.reload(lecturer)
        all_courses = lecturer.course_id
        for course in all_courses:
            course.update(set__is_activating = False)
            Course.reload(course)
        return redirect(url_for("admin_show_all_lecturers"))
    else:
        return redirect(url_for("user_sign_in"))

#. Active Lecturer
@app.route("/admin/active-lecturer/<lecturer_id>")
def admin_active_lecturer(lecturer_id):
    if "admin_signed_in" in session:
        lecturer = Lecturer.objects.with_id(lecturer_id)
        lecturer.update(set__is_activating = True)
        Lecturer.reload(lecturer)
        all_courses = lecturer.course_id
        for course in all_courses:
            course.update(set__is_activating = True)
            Course.reload(course)
        return redirect(url_for("admin_show_all_lecturers"))
    else:
        return redirect(url_for("user_sign_in"))

#. Delete Course
@app.route("/admin/del-course/<course_id>")
def admin_del_course(course_id):
    if "admin_signed_in" in session:
        course = Course.objects.with_id(course_id)
        course.update(set__is_activating = False)
        Course.reload(course)
        return redirect("admin_show_courses")
    else:
        return redirect(url_for("user_sign_in"))

#. Active Course
@app.route("/admin/active-course/<course_id>")
def admin_active_course(course_id):
    if "admin_signed_in" in session:
        course = Course.objects.with_id(course_id)
        course.update(set__is_activating = True)
        Course.reload()
        return redirect("admin_show_all_courses")
    else:
        return redirect(url_for("user_sign_in"))

# ---CUSTOMER---
#. Customer profile
@app.route("/customer-proflie/<customer_id>")
def customer_profile(customer_id):
    if "customer_signed_in" in session:
        customer = User.objects.with_id(customer_id)
        all_purchased_courses = Order.objects(customer_id__exact = customer_id, is_purchased = True)
        return render_template("user/customer/customer-profile.html", customer = customer, 
        all_purchased_courses = all_purchased_courses)
    else:
        return redirect(url_for("user_sign_in"))

#. Update profile
@app.route("/customer-profile/update-profile/<customer_id>", methods = ["GET", "POST"])
def update_profile(customer_id):
    customer = User.objects.with_id(customer_id)
    if request.method == "GET":
        if "customer_signed_in" in session:
            return render_template("user/customer/update-profile.html", customer = customer)
        else:
            return redirect(url_for("user_sign_in"))
    elif request.method == "POST":
        form = request.form
        name = form["name"]
        email = form["email"]
        phone_number = form["phone-number"]
        customer.update(set__name = name, set__email = email, set__phone_number = phone_number)
        User.reload(customer)
        return redirect(url_for("customer_profile", customer_id = session["customer_signed_in_id"]))

#. Course content
@app.route("/course-content/<course_id>")
def course_content(course_id):
    if "customer_signed_in" in session:
        course = Course.objects.with_id(course_id)
        all_lessons = course.lesson_id
        ydl = YoutubeDL()
        list_videos = []
        for lesson in all_lessons:
            video_info = {}
            video_title = lesson.name 
            data = ydl.extract_info(lesson.link, download = False)
            video_id = data["id"]
            video_info[video_title] = video_id
            list_videos.append(video_info)
    return render_template("user/customer/course-content.html", course = course, 
    all_lessons = all_lessons, list_videos = list_videos)

#. Lecturer info
@app.route("/show-all-lecturers")
def lecturer_info():
    if "customer_signed_in" in session:
        all_lecturers = Lecturer.objects(is_activating = True)
        return render_template("page/lecturer-info.html",
        all_lecturers = all_lecturers)
    else:
        return redirect(url_for("user_sign_in"))

#. Lecturer detail
@app.route("/lecturer-detail/<lecturer_id>")
def lecturer_detail(lecturer_id):
    if "customer_signed_in" in session:
        lecturer = Lecturer.objects.with_id(lecturer_id)
        all_courses = lecturer.course_id
        return render_template("page/lecturer-detail.html", 
        lecturer = lecturer, all_courses = all_courses)
    else:
        return redirect(url_for("user_sign_in"))

#. Show all categories
@app.route("/show-all-categories")
def show_all_categories():
    if "customer_signed_in" in session:
        all_categories = Category.objects()
        return render_template("page/show-all-categories.html", all_categories = all_categories)
    elif "admin_signed_in" in session:
        all_categories = Category.objects()
        return render_template("page/show-all-categories.html", all_categories = all_categories)
    else:
        return redirect(url_for("user_sign_in"))

#. Courses info
@app.route("/courses-info/<category_id>")
def course_info(category_id):
    if "customer_signed_in" in session:
        all_courses = Course.objects(category_id = category_id, is_activating = True)
        return render_template("page/course-info.html", all_courses = all_courses)

#. Customer sign up
@app.route("/user/user-sign-up", methods = ["GET", "POST"])
def customer_sign_up():
    error = None
    if request.method == "GET":
        return render_template("user/customer/customer-sign-up.html")
    elif request.method == "POST":
        form = request.form
        name = form["name"]
        email = form["email"]
        sign_up = form["sign-up"]
        password = form["password"]
        new_customer = User(
            name = name,
            sign_in = sign_up,
            email = email,
            password = password,
        )
        new_customer.save()
        User.reload(new_customer)
        return redirect(url_for("user_sign_in"))

#. Detail Course (Customer)
@app.route("/course-detail/<course_id>")
def course_detail(course_id):
    if "customer_signed_in" in session:
        checking = None
        course = Course.objects.with_id(course_id)
        list_orders = Order.objects(customer_id = session["customer_signed_in_id"], course_id = course_id)
        all_lessons = course.lesson_id
        lesson_demo = all_lessons[0]
        list_lecturers = Lecturer.objects(course_id = course_id)
        lecturer = list_lecturers[0]
        ydl = YoutubeDL()
        data = ydl.extract_info(lesson_demo.link, download = False)
        video_id = data["id"]
        if len(list_orders) != 0:
            order = list_orders[0]
            if order.is_purchased:
                checking = ("purchased")
                return render_template("page/course-detail.html", 
                course = course, all_lessons = all_lessons, lecturer = lecturer,
                checking = checking, video_id = video_id)
            elif order.is_purchased == False:
                checking = ("not_purchased")
                return render_template("page/course-detail.html", 
                course = course, all_lessons = all_lessons, lecturer = lecturer,
                checking = checking, video_id = video_id)
        elif len(list_orders) == 0:
            checking = ("not_order")
            return render_template("page/course-detail.html", course = course, 
            all_lessons = all_lessons, lecturer = lecturer, checking = checking,
            video_id = video_id)

#. Order course 
@app.route("/order_course/<course_id>/<customer_id>")
def order_course(course_id, customer_id):
    if "customer_signed_in" in session:
        order = Order.objects(course_id__exact = course_id, customer_id__exact = customer_id, is_purchased = False)
        if len(order) != 0:
            return render_template("page/confirmed-order.html") 
        elif len(order) == 0:
            new_order = Order(
                order_time = datetime.now(),
                course_id = course_id,
                customer_id = customer_id,
            )
            new_order.save()
            Order.reload(new_order)
            return render_template("page/ordered-course.html")

#. User sign out
@app.route("/user/user-sign-out")
def user_sign_out():    
    if "admin_signed_in" in session:
        del session["admin_signed_in"]
    elif "customer_signed_in" in session: 
        del session["customer_signed_in"]
    return redirect(url_for("homepage"))

# ---PAGE---
#. Category
@app.route("/category/esport")
def esport():
    return render_template("category/esport.html")

#. Route Music
@app.route("/category/music")    
def music():
    return render_template("category/music.html")

#. Route Sport
@app.route("/category/sport")
def sport():
    return render_template("category/sport.html")

#. Introduction
#. Route Gym
@app.route("/introduction/gym")
def gym():
    return render_template("category/introduction/what-is-gym.html")

#. Route LOL
@app.route("/introduction/lol")
def lol():
    return render_template("category/introduction/what-is-lol.html")

#. Route PES
@app.route("/introduction/pes")
def pes():
   return render_template("category/introduction/what-is-pes.html")

#. Route DOTA2
@app.route("/introduction/dota2")
def dota2():
    return render_template("category/introduction/what-is-dota2.html")

@app.route("/introduction/football")
def football():
    return render_template("category/introduction/what-is-football.html")

#. Route Basketball
@app.route("/introduction/basketball")
def basketball():
    return render_template("category/introduction/what-is-basketball.html")

#. Route Guitar
@app.route("/introduction/guitar")
def guitar():
    return render_template("category/introduction/what-is-guitar.html")

#. Route Piano
@app.route("/introduction/piano")
def piano():
    return render_template("category/introduction/what-is-piano.html")

#. Route Ukulele
@app.route("/introduction/ukulele")
def ukulele():
    return render_template("category/introduction/what-is-ukulele.html")

#. Basic knowlegde
#. Route Football
@app.route("/basic-learing/football")
def basic_learning_football():
    return render_template("category/basic-knowledge/basic-learning-football.html")

#. Route Basketball
@app.route("/basic-learing/basketball")
def basic_learning_basketball():
    return render_template("category/basic-knowledge/basic-learning-basketball.html")

#. Route Guitar
@app.route("/basic-learing/guitar")
def basic_learning_guitar():
    return render_template("category/basic-knowledge/basic-learning-guitar.html")

#. Route Gym
@app.route("/basic-learing/gym")
def basic_learning_gym():
    return render_template("category/basic-knowledge/basic-learning-gym.html")

#. Route LOL
@app.route("/basic-learing/lol")
def basic_learning_lol():
    return render_template ("category/basic-knowledge/basic-learning-lol.html")

#. Route PES
@app.route("/basic-learing/pes")
def basic_learning_pes():
    return render_template("category/basic-knowledge/basic-learning-pes.html")

@app.route("/basic-learning/piano")
def basic_learning_piano():
    return render_template("category/basic-knowledge/basic-learning-piano.html")

#. Route Dota 2
@app.route("/basic-learing/dota2")
def basic_learning_dota2():
    return render_template("category/basic-knowledge/basic-learning-dota2.html")

# @lia_app.route("/test")
# def test():
#     course_id = "5b93836bfd2b0f0460b11778"
#     course = Course.objects.with_id(course_id)
#     return render_template("page/testing.html", course = course)

if __name__ == '__main__':
    app.run(debug=True)

