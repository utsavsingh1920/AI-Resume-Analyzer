import streamlit as st
import pandas as pd
import base64, random
import time, datetime
import sqlite3
import os
import socket
import platform
import geocoder
import secrets
import io
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from resume_parser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import nltk
nltk.download('stopwords')


# Try loading en_core_web_sm and download if missing
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     download("en_core_web_sm")
    # nlp = spacy.load("en_core_web_sm")

# Connect to SQLite database
connection = sqlite3.connect('resume_analyzer.db')
cursor = connection.cursor()

###### Preprocessing functions ######

def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

###### Database Functions ######

def insert_data(sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, act_name, act_mail, act_mob, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses, pdf_name):
    insert_sql = """INSERT INTO user_data (
        sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, 
        act_name, act_mail, act_mob, Name, Email_ID, resume_score, Timestamp, Page_no, 
        Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses, pdf_name
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    rec_values = (str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, str(latlong), city, state, country, 
                  act_name, act_mail, act_mob, name, email, str(res_score), timestamp, str(no_of_pages), 
                  reco_field, cand_level, str(skills), str(recommended_skills), str(courses), pdf_name)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def insertf_data(feed_name, feed_email, feed_score, comments, Timestamp):
    insertfeed_sql = """INSERT INTO user_feedback (
        feed_name, feed_email, feed_score, comments, Timestamp
    ) VALUES (?, ?, ?, ?, ?)"""
    rec_values = (feed_name, feed_email, str(feed_score), comments, Timestamp)
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()

###### Setting Page Configuration ######

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon='./Logo/recommend.png',
)

###### Main function run() ######

geolocator = Nominatim(
    user_agent="resume-analyzer-app",
    timeout=10
)

def safe_reverse_geocode(latlong):
    try:
        location = geolocator.reverse(latlong, language="en")
        return location   # ✅ return full object
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None


def run():
    img = Image.open('./Logo/Updatelight.jpeg')
    # video = st.video('./Logo/Resume-Analyzer.mp4')

    # st.image(video)
    st.image(img)
    st.sidebar.markdown("# Choose Something...")
    activities = ["User", "Feedback", "About", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    link = '<b>Built with 🤍 by <a href="https://dnoobnerd.netlify.app/" style="text-decoration: none; color: #4587f7;">Utsav Singh</a></b>' 
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.markdown('''
        <div id="sfct2xghr8ak6lfqt3kgru233378jya38dy" hidden></div>
        <noscript>
            <a href="https://www.freecounterstat.com" title="hit counter">
                <img src="https://counter9.stat.ovh/private/freecounterstat.php?c=t2xghr8ak6lfqt3kgru233378jya38dy" border="0" title="hit counter" alt="hit counter">
            </a>
        </noscript>
        <p>Visitors <img src="https://counter9.stat.ovh/private/freecounterstat.php?c=t2xghr8ak6lfqt3kgru233378jya38dy" title="Free Counter" Alt="web counter" width="60px" border="0" /></p>
    ''', unsafe_allow_html=True)

    # Create tables
    cursor.execute("""
    SELECT
        ID,
        sec_token,
        ip_add,
        act_name,
        act_mail,
        act_mob,
        Predicted_Field,
        Timestamp,
        Name,
        Email_ID,
        resume_score,
        Page_no,
        pdf_name,
        User_level,
        Actual_skills,
        Recommended_skills,
        Recommended_courses,
        city,
        state,
        country,
        latlong,
        os_name_ver,
        host_name,
        dev_user
    FROM user_data
    """)

    data = cursor.fetchall()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_feedback (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                feed_name TEXT NOT NULL,
                feed_email TEXT NOT NULL,
                feed_score TEXT NOT NULL,
                comments TEXT,
                Timestamp TEXT NOT NULL
            )""")
    connection.commit()

    ###### CODE FOR CLIENT SIDE (USER) ######
    if choice == 'User':
        act_name = st.text_input('Name*')
        act_mail = st.text_input('Mail*')
        act_mob = st.text_input('Mobile Number*')
        sec_token = secrets.token_urlsafe(12)
        host_name = socket.gethostname()
        ip_add = socket.gethostbyname(host_name)
        dev_user = os.getlogin()
        os_name_ver = platform.system() + " " + platform.release()
        g = geocoder.ip('me')
        latlong = g.latlng
        geolocator = Nominatim(user_agent="http")
        # location = geolocator.reverse(latlong, language='en')
        location = safe_reverse_geocode(latlong)

        if location and hasattr(location, "raw"):
            address = location.raw.get("address", {})
            city = address.get("city", address.get("town", address.get("village", "")))
            state = address.get("state", "")
            country = address.get("country", "")
        else:
          city = state = country = "Unknown"
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')

        st.markdown('''<h5 style='text-align: left; color: #4587f7;'> Upload Your Resume, And Get Smart Recommendations</h5>''', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Hang On While We Cook Magic For You...'):
                time.sleep(4)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            pdf_name = pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                resume_text = pdf_reader(save_image_path)
                st.header("**Resume Analysis 🤘**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info 👀**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Degree: ' + str(resume_data['degree']))
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] < 1:
                    cand_level = "NA"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
                elif 'INTERNSHIP' in resume_text or 'Internship' in resume_text or 'INTERNSHIPS' in resume_text or 'Internships' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)
                elif 'EXPERIENCE' in resume_text or 'Experience' in resume_text or 'WORK EXPERIENCE' in resume_text or 'Work Experience' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!</h4>''', unsafe_allow_html=True)
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
                st.subheader("**Skills Recommendation 💡**")
                keywords = st_tags(label='### Your Current Skills', text='See our skills recommendation below', value=resume_data['skills'], key='1')
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'C#', 'Asp.net', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']
                n_any = ['english', 'communication', 'writing', 'microsoft office', 'leadership', 'customer management', 'social media']
                recommended_skills = []
                reco_field = ''
                rec_course = ''
                for i in resume_data['skills']:
                    if i.lower() in ds_keyword:
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining', 'Clustering & Classification', 'Data Analytics', 'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras', 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask", 'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='2')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break
                    elif i.lower() in web_keyword:
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='3')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break
                    elif i.lower() in android_keyword:
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java', 'Kivy', 'GIT', 'SDK', 'SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='4')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break
                    elif i.lower() in ios_keyword:
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode', 'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation', 'Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='5')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break
                    elif i.lower() in uiux_keyword:
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing', 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='6')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break
                    elif i.lower() in n_any:
                        reco_field = 'NA'
                        st.warning("** Currently our tool only predicts and recommends for Data Science, Web, Android, IOS and UI/UX Development**")
                        recommended_skills = ['No Recommendations']
                        recommended_keywords = st_tags(label='### Recommended skills for you.', text='Currently No Recommendations', value=recommended_skills, key='6')
                        st.markdown('''<h5 style='text-align: left; color: #092851;'>Maybe Available in Future Updates</h5>''', unsafe_allow_html=True)
                        rec_course = "Sorry! Not Available for this Field"
                        break
                st.subheader("**Resume Tips & Ideas 🥂**")
                resume_score = 0
                if 'Objective' in resume_text or 'Summary' in resume_text:
                    resume_score += 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h5>''', unsafe_allow_html=True)
                if 'Education' in resume_text or 'School' in resume_text or 'College' in resume_text:
       
                    resume_score += 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h5>''', unsafe_allow_html=True)
                if 'EXPERIENCE' in resume_text or 'Experience' in resume_text or 'WORK EXPERIENCE' in resume_text or 'Work Experience' in resume_text:
                    resume_score += 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #ffffff;'>[-] Please add Experience. It will help you to stand out from crowd</h5>''', unsafe_allow_html=True)
                if 'INTERNSHIPS' in resume_text or 'INTERNSHIP' in resume_text or 'Internships' in resume_text or 'Internship' in resume_text:
                    resume_score += 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #5def4d;'>[-] Please add Internships. It will help you to stand out from crowd</h5>''', unsafe_allow_html=True)
                if 'SKILLS' in resume_text or 'SKILL' in resume_text or 'Skills' in resume_text or 'Skill' in resume_text:
                    resume_score += 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #5def4d;'>[-] Please add Skills. It will help you a lot</h5>''', unsafe_allow_html=True)
                if 'HOBBIES' in resume_text or 'Hobbies' in resume_text:
                    resume_score += 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #5def4d;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h5>''', unsafe_allow_html=True)
                if 'INTERESTS' in resume_text or 'Interests' in resume_text:
                    resume_score += 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #5def4d;'>[-] Please add Interest. It will show your interest other that job.</h5>''', unsafe_allow_html=True)
                if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text:
                    resume_score += 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #5def4d;'>[-] Please add Achievements. It will show that you are capable for the required position.</h5>''', unsafe_allow_html=True)
                if 'CERTIFICATIONS' in resume_text or 'Certifications' in resume_text or 'Certification' in resume_text:
                    resume_score += 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:#5def4d;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h5>''', unsafe_allow_html=True)
                if 'PROJECTS' in resume_text or 'PROJECT' in resume_text or 'Projects' in resume_text or 'Project' in resume_text:
                    resume_score += 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:#5def4d;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h5>''', unsafe_allow_html=True)
                st.subheader("**Resume Score 📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)
                insert_data(str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, latlong, city, state, country, act_name, act_mail, act_mob, resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, resume_data['skills'], recommended_skills, rec_course, pdf_name)
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                st.video(resume_vid)
                st.header("**Bonus Video for Interview Tips💡**")
                interview_vid = random.choice(interview_videos)
                st.video(interview_vid)
                st.balloons()
            else:
                st.error('Something went wrong..')
    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date + '_' + cur_time)
        with st.form("my_form"):
            st.write("Feedback form")
            feed_name = st.text_input('Name')
            feed_email = st.text_input('Email')
            feed_score = st.slider('Rate Us From 1 - 5', 1, 5)
            comments = st.text_input('Comments')
            Timestamp = timestamp
            submitted = st.form_submit_button("Submit")
            if submitted:
                insertf_data(feed_name, feed_email, feed_score, comments, Timestamp)
                st.success("Thanks! Your Feedback was recorded.")
                st.balloons()
        query = 'SELECT * FROM user_feedback'
        plotfeed_data = pd.read_sql(query, connection)
        labels = plotfeed_data.feed_score.unique()
        values = plotfeed_data.feed_score.value_counts()
        st.subheader("**Past User Rating's**")
        fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5", color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig)
        cursor.execute('SELECT feed_name, comments FROM user_feedback')
        plfeed_cmt_data = cursor.fetchall()
        st.subheader("**User Comment's**")
        dff = pd.DataFrame(plfeed_cmt_data, columns=['User', 'Comment'])
        st.dataframe(dff, width=1000)
    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':
        st.subheader("**About The Tool - AI RESUME ANALYZER**")
        st.markdown('''
        <p align='justify'>
            A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. And lastly show recommendations, predictions, analytics to the applicant based on keyword matching.
        </p>
        <p align="justify">
            <b>How to use it: -</b> <br/><br/>
            <b>User -</b> <br/>
            In the Side Bar choose yourself as user and fill the required fields and upload your resume in pdf format.<br/>
            Just sit back and relax our tool will do the magic on it's own.<br/><br/>
            <b>Feedback -</b> <br/>
            A place where user can suggest some feedback about the tool.<br/><br/>
            <b>Admin -</b> <br/>
            For login use <b>admin</b> as username and <b>admin@resume-analyzer</b> as password.<br/>
            It will load all the required stuffs and perform analysis.
        </p><br/><br/>
        <p align="justify">
            Built with 🤍 by 
            <a href="https://dnoobnerd.netlify.app/" style="text-decoration: none; color: grey;">Utsav Singh</a> through 
            <a href="https://www.linkedin.com/in/utsav-singh-951651295/" style="text-decoration: none; color: grey;">Dr Bright --(Web Developer)</a>
        </p>
        ''', unsafe_allow_html=True)
 
    
    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':   

        st.subheader("**About The Tool - AI RESUME ANALYZER**")

        st.markdown('''

        <p align='justify'>
            A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. And lastly show recommendations, predictions, analytics to the applicant based on keyword matching.
        </p>

        <p align="justify">
            <b>How to use it: -</b> <br/><br/>
            <b>User -</b> <br/>
            In the Side Bar choose yourself as user and fill the required fields and upload your resume in pdf format.<br/>
            Just sit back and relax our tool will do the magic on it's own.<br/><br/>
            <b>Feedback -</b> <br/>
            A place where user can suggest some feedback about the tool.<br/><br/>
            <b>Admin -</b> <br/>
            For login use <b>admin</b> as username and <b>admin@resume-analyzer</b> as password.<br/>
            It will load all the required stuffs and perform analysis.
        </p><br/><br/>

        <p align="justify">
            Built with 🤍 by 
            <a href="https://dnoobnerd.netlify.app/" style="text-decoration: none; color: grey;">Utsav Singh</a> through 
            <a href="https://www.linkedin.com/in/utsav-singh-951651295/" style="text-decoration: none; color: grey;">Dr Bright --(Web Developer)</a>
        </p>

        ''',unsafe_allow_html=True)  


    ###### CODE FOR ADMIN SIDE (ADMIN) ######
    else:
        st.success('Welcome to Admin Side')

        #  Admin Login
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')

        if st.button('Login'):
            
            ## Credentials 
            if ad_user == 'admin' and ad_password == 'admin':
                
                ### Fetch miscellaneous data from user_data(table) and convert it into dataframe
                # cursor.execute('''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8), convert(User_level using utf8), city, state, country from user_data''')
                cursor.execute("""
                SELECT
                    ID,
                    sec_token,
                    ip_add,
                    act_name,
                    act_mail,
                    act_mob,
                    Predicted_Field,
                    Timestamp,
                    Name,
                    Email_ID,
                    resume_score,
                    Page_no,
                    pdf_name,
                    User_level,
                    Actual_skills,
                    Recommended_skills,
                    Recommended_courses,
                    city,
                    state,
                    country,
                    latlong,
                    os_name_ver,
                    host_name,
                    dev_user
                FROM user_data
                """)

                # data = cursor.fetchall()

                datanalys = cursor.fetchall()
                plot_data = pd.DataFrame(datanalys, columns=[
                    'ID', 'Token', 'IP_add', 'Act Name', 'Act Mail', 'Act Mob', 'Predicted_Field', 'Timestamp',
                    'Name', 'Email_ID', 'resume_score', 'Page_no', 'pdf_name', 'User_Level', 'Actual_Skills',
                    'Recommended_Skills', 'Recommended_Courses', 'City', 'State', 'Country', 'LatLong',
                    'OS_Name', 'Host_Name', 'Dev_User'
                ])

                values = plot_data.ID.count()

                # values = plot_data['ID'].count()
                st.success("Welcome to CodeMaking Thanks to see this AI ! Total %d " % values + " User's Have Used Our Tool : )")                
                
                ### Fetch user data from user_data(table) and convert it into dataframe
                cursor.execute('''
                SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob,
                    Predicted_Field, Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name,
                    User_level, Actual_skills, Recommended_skills, Recommended_courses,
                    city, state, country, latlong, os_name_ver, host_name, dev_user
                FROM user_data
                ''')
                data = cursor.fetchall()

                st.header("**User's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Token', 'IP Address', 'Name', 'Mail', 'Mobile Number', 'Predicted Field', 'Timestamp',
                                                 'Predicted Name', 'Predicted Mail', 'Resume Score', 'Total Page',  'File Name',   
                                                 'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course',
                                                 'City', 'State', 'Country', 'Lat Long', 'Server OS', 'Server Name', 'Server User',])
                
                ### Viewing the dataframe
                st.dataframe(df)
                
                ### Downloading Report of user_data in csv file
                st.markdown(get_csv_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)

                ### Fetch feedback data from user_feedback(table) and convert it into dataframe
                cursor.execute('''SELECT * from user_feedback''')
                data = cursor.fetchall()

                st.header("**User's Feedback Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Feedback Score', 'Comments', 'Timestamp'])
                st.dataframe(df)

                ### query to fetch data from user_feedback(table)
                query = 'select * from user_feedback'
                plotfeed_data = pd.read_sql(query, connection)                        

                ### Analyzing All the Data's in pie charts

                # fetching feed_score from the query and getting the unique values and total value count 
                labels = plotfeed_data.feed_score.unique()
                values = plotfeed_data.feed_score.value_counts()
                
                # Pie chart for user ratings
                st.subheader("**User Rating's**")
                fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5 🤗", color_discrete_sequence=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig)

                # fetching Predicted_Field from the query and getting the unique values and total value count                 
                labels = plot_data.Predicted_Field.unique()
                values = plot_data.Predicted_Field.value_counts()

                # Pie chart for predicted field recommendations
                st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills 👽', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
                st.plotly_chart(fig)

                # fetching User_Level from the query and getting the unique values and total value count                 
                labels = plot_data.User_Level.unique()
                values = plot_data.User_Level.value_counts()

                # Pie chart for User's👨‍💻 Experienced Level
                st.subheader("**Pie-Chart for User's Experienced Level**")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart 📈 for User's 👨‍💻 Experienced Level", color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig)

                # fetching resume_score from the query and getting the unique values and total value count                 
                labels = plot_data.resume_score.unique()                
                values = plot_data.resume_score.value_counts()

                # Pie chart for Resume Score
                st.subheader("**Pie-Chart for Resume Score**")
                fig = px.pie(df, values=values, names=labels, title='From 1 to 100 💯', color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig)

                # fetching IP_add from the query and getting the unique values and total value count 
                labels = plot_data.IP_add.unique()
                values = plot_data.IP_add.value_counts()

                # Pie chart for Users
                st.subheader("**Pie-Chart for Users App Used Count**")
                fig = px.pie(df, values=values, names=labels, title='Usage Based On IP Address 👥', color_discrete_sequence=px.colors.sequential.matter_r)
                st.plotly_chart(fig)

                # fetching City from the query and getting the unique values and total value count 
                labels = plot_data.City.unique()
                values = plot_data.City.value_counts()

                # Pie chart for City
                st.subheader("**Pie-Chart for City**")
                fig = px.pie(df, values=values, names=labels, title='Usage Based On City 🌆', color_discrete_sequence=px.colors.sequential.Jet)
                st.plotly_chart(fig)

                # fetching State from the query and getting the unique values and total value count 
                labels = plot_data.State.unique()
                values = plot_data.State.value_counts()

                # Pie chart for State
                st.subheader("**Pie-Chart for State**")
                fig = px.pie(df, values=values, names=labels, title='Usage Based on State 🚉', color_discrete_sequence=px.colors.sequential.PuBu_r)
                st.plotly_chart(fig)

                # fetching Country from the query and getting the unique values and total value count 
                labels = plot_data.Country.unique()
                values = plot_data.Country.value_counts()

                # Pie chart for Country
                st.subheader("**Pie-Chart for Country**")
                fig = px.pie(df, values=values, names=labels, title='Usage Based on Country 🌏', color_discrete_sequence=px.colors.sequential.Purpor_r)
                st.plotly_chart(fig)

            ## For Wrong Credentials
            else:
                st.error("Wrong ID & Password Provided")

# Calling the main (run()) function to make the whole process run
run()




# @CodeMaking05