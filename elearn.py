import requests
from bs4 import BeautifulSoup

cnuportal_login = 'https://portal.cnu.ac.kr/enview/user/login.face'
elearning_redirection = 'http://e-learn.cnu.ac.kr/ksign/index.jsp'
elearning_myLecture = 'http://e-learn.cnu.ac.kr/lms/myLecture/doListView.dunet'
elearning_myClassroom = 'http://e-learn.cnu.ac.kr/lms/class/classroom/doViewClassRoom_new.dunet'
classroom_course = 'http://e-learn.cnu.ac.kr/lms/class/courseSchedule/doListView.dunet'

subject_dict = dict()
subject_percentage = list()

def dict_show(dict):
	for key, value in dict.items():
		print(key, end='|')
		print(value['name'], end='\t|')
		print(value['percentage'], end='\t|')
		print('미진행', value['unseen'], end='\t|')
		print('시작전', value['notyet'], end='\t')
		print()

def main():
	with requests.Session() as s:
		print('***Login portal.cnu.ac.kr***')
		id_cnuportal = input('ID : ')
		pw_cnuportal = input('PW : ')

		LOGIN_INFO = {
			'userId': id_cnuportal,
			'password': pw_cnuportal
		}

		login = s.post(cnuportal_login, data=LOGIN_INFO)
		elearn = s.get(elearning_redirection, verify=False)
		myLecture = s.get(elearning_myLecture, verify=False)

		elearn_html = myLecture.text
		elearn_soup = BeautifulSoup(elearn_html, 'html.parser')
		subjects = elearn_soup.find_all('a', {'class':'classin2'})

		i = 0
		for subject in subjects:
			subject_dict[i] = {
				'id': subject.get('course_id'),
				'no': subject.get('class_no'),
				'name': "",
				'percentage' : "",
				'unseen' : "",
				'notyet' : ""
			}
			i += 1

		for key, value in subject_dict.items():
			CLASS_INFO = {
				'mnid': '201008840728',
				'course_id': value['id'],
				'class_no': value['no']
			}

			classroom = s.post(elearning_myClassroom, data=CLASS_INFO)
			classroom_html = classroom.text
			classroom_soup = BeautifulSoup(classroom_html, 'html.parser')
			class_percentage = classroom_soup.find('span', {'class':"num"}).text
			subject_percentage.append(class_percentage)

			course = s.get(classroom_course, verify=False)
			course_html = course.text
			course_soup = BeautifulSoup(course_html, 'html.parser')
			course_name = course_soup.find('p', {'class':"list_tit"}).text
			subject_dict[key]['name'] = course_name
			subject_dict[key]['percentage'] = subject_percentage[key]

			lectures = course_soup.find_all('td')

			unseen = 0
			notyet = 0
			for lecture in lectures :
				if lecture.text.find('미진행') != -1:
					unseen += 1
				if lecture.text.find('학습시작전') != -1:
					unseen -= 1
					notyet += 1

			subject_dict[key]['unseen'] = unseen
			subject_dict[key]['notyet'] = notyet

		dict_show(subject_dict)

if __name__=='__main__':
	main()