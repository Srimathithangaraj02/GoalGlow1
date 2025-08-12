from app import db
from app import app
from models import CareerGoal, Skill, Resource

def run_seed():
    db.drop_all()  # Clears existing tables (CAUTION: Deletes old data)
    db.create_all()

    # =====================
    # Career Goals & Skills
    # =====================
    goals_data = {
        "Full Stack Developer": {
            "skills": {
                "HTML": [
                    ("W3Schools HTML", "https://www.w3schools.com/html/"),
                    ("HTML MDN Docs", "https://developer.mozilla.org/en-US/docs/Web/HTML")
                ],
                "CSS": [
                    ("W3Schools CSS", "https://www.w3schools.com/css/"),
                    ("CSS Tricks", "https://css-tricks.com/")
                ],
                "JavaScript": [
                    ("JavaScript Guide - MDN", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
                    ("JavaScript Tutorial", "https://www.javascripttutorial.net/")
                ],
                "Python": [
                    ("Python Official Docs", "https://docs.python.org/3/"),
                    ("Learn Python", "https://www.learnpython.org/")
                ],
                "Flask": [
                    ("Flask Docs", "https://flask.palletsprojects.com/"),
                    ("Flask Tutorial", "https://www.tutorialspoint.com/flask/index.htm")
                ]
            }
        },
        "Data Scientist": {
            "skills": {
                "Python": [
                    ("Python Docs", "https://docs.python.org/3/"),
                    ("Learn Python", "https://www.learnpython.org/")
                ],
                "Pandas": [
                    ("Pandas Docs", "https://pandas.pydata.org/docs/"),
                    ("Pandas Tutorial", "https://www.datacamp.com/courses/pandas-foundations")
                ],
                "NumPy": [
                    ("NumPy Docs", "https://numpy.org/doc/"),
                    ("NumPy Tutorial", "https://www.w3schools.com/python/numpy/default.asp")
                ],
                "Matplotlib": [
                    ("Matplotlib Docs", "https://matplotlib.org/stable/contents.html"),
                    ("Matplotlib Tutorial", "https://www.datacamp.com/community/tutorials/matplotlib-tutorial-python")
                ],
                "Machine Learning": [
                    ("Scikit-Learn Docs", "https://scikit-learn.org/stable/"),
                    ("Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course")
                ]
            }
        },
        "AI/ML Engineer": {
            "skills": {
                "Python": [
                    ("Learn Python", "https://www.learnpython.org/"),
                    ("Python Docs", "https://docs.python.org/3/")
                ],
                "TensorFlow": [
                    ("TensorFlow Docs", "https://www.tensorflow.org/learn"),
                    ("TensorFlow YouTube", "https://www.youtube.com/@TensorFlow")
                ],
                "PyTorch": [
                    ("PyTorch Docs", "https://pytorch.org/docs/stable/index.html"),
                    ("PyTorch Tutorials", "https://pytorch.org/tutorials/")
                ],
                "Deep Learning": [
                    ("Deep Learning Specialization", "https://www.coursera.org/specializations/deep-learning"),
                    ("Fast.ai", "https://course.fast.ai/")
                ],
                "Data Preprocessing": [
                    ("Data Preprocessing Tutorial", "https://www.javatpoint.com/data-preprocessing-in-machine-learning"),
                    ("Feature Engineering", "https://www.kaggle.com/learn/feature-engineering")
                ]
            }
        },
        "Cyber Security Analyst": {
            "skills": {
                "Networking Basics": [
                    ("Computer Networking", "https://www.geeksforgeeks.org/computer-network-tutorials/"),
                    ("Cisco Networking Basics", "https://www.cisco.com/c/en/us/training-events/training-certifications/exams/current-list/ccna.html")
                ],
                "Linux": [
                    ("Linux Basics", "https://linuxjourney.com/"),
                    ("Linux Command Line", "https://www.codecademy.com/learn/learn-the-command-line")
                ],
                "Cryptography": [
                    ("Cryptography Basics", "https://www.tutorialspoint.com/cryptography/index.htm"),
                    ("Applied Cryptography", "https://crypto.stackexchange.com/")
                ],
                "Ethical Hacking": [
                    ("CEH Prep", "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/"),
                    ("Hack The Box", "https://www.hackthebox.com/")
                ],
                "Incident Response": [
                    ("Incident Response Guide", "https://www.cisa.gov/incident-response"),
                    ("NIST Incident Handling", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf")
                ]
            }
        },
        "Cloud Computing Specialist": {
            "skills": {
                "AWS": [
                    ("AWS Training", "https://aws.amazon.com/training/"),
                    ("AWS YouTube", "https://www.youtube.com/@aws")
                ],
                "Azure": [
                    ("Azure Training", "https://learn.microsoft.com/en-us/training/"),
                    ("Azure YouTube", "https://www.youtube.com/@MicrosoftAzure")
                ],
                "Google Cloud": [
                    ("GCP Training", "https://cloud.google.com/training"),
                    ("Google Cloud YouTube", "https://www.youtube.com/@googlecloud")
                ],
                "Docker": [
                    ("Docker Docs", "https://docs.docker.com/"),
                    ("Docker Tutorial", "https://www.tutorialspoint.com/docker/index.htm")
                ],
                "Kubernetes": [
                    ("Kubernetes Docs", "https://kubernetes.io/docs/"),
                    ("Kubernetes Tutorial", "https://www.tutorialspoint.com/kubernetes/index.htm")
                ]
            }
        }
    }

    # =====================
    # Insert Data into DB
    # =====================
    for goal_name, goal_data in goals_data.items():
        goal = CareerGoal(name=goal_name)
        db.session.add(goal)
        db.session.flush()

        for skill_name, resources in goal_data["skills"].items():
            skill = Skill(name=skill_name, career_goal_id=goal.id)
            db.session.add(skill)
            db.session.flush()

            for res_title, res_url in resources:
                res = Resource(skill_id=skill.id, title=res_title, url=res_url)
                db.session.add(res)

    db.session.commit()
    print("✅ Database seeded successfully with all career goals!")

if __name__ == "__main__":
    with app.app_context():
        run_seed()