## Fiala
# School Management Application 

Remmeber during deployment to initiate creating the various groups either programmatically or from the django admin portal 
Remember to add the permissions on the various classes on the API



Password reset should be done by admin
User groups done. 
Next is Linking Students to Parents.  DONE 
	* Then linking Teachers classes and subjects; 
		For this, Admin creates the Teacher and creates a subject then adds the created teacher. 
	* Student to classes - DONE
User Profile on the main page - Accessible by all


Admin Portal
* List Users - Username and Role
	* Change Password
	* Edit User (class)/Subjects
	* Add a remark on Student user (Admin/Teacher)
	* Add a subject. 
* Upload Time Table 
* Add a PTA Minute
* Schedule a PTA Meeting 
* 


Teacher's View
* List of Classes
	* List of Subjects
		* List of Students registered for that subject
		* Add Textbook 
		* Upload Assignment 
		* View Time Table

Student's View 
* List of Subjects/Courses
	* Assignments (New, Submitted and Graded)
	* Text Books - Download 
	* View Time table 
	* 



Schools register on the platform and an admin is created. They can request multiple admins. 
User management
	* School Admin 
	* Teachers 
	* Students 
	* Parents 

Every school will be created with an admin. 
* Admins will be given the right to add users. 
* A temporary password is created for each user created 
* A role is assigned to the user, (Admin, Student, Teacher, ParentOrGuardian)
	* Students
		* When students are created, they will be assigned to their current classes. 
		* When the Student logs in, they will have the sourses/subjects registered under their class in the school 


	* Teachers
		* Teachers are assigned courses/subjects when they are created. A teacher must be available before a subject is created. If the teacher ceases to exist in the system, the subject will not be active. 
		* Teachers can see all students under their courses/subjects. 
		* A teachers portal will have a list of all courses/subjects they have been assigned. Since courses/subjects are divided based on classes/levels. 
		* Each course/subject will have their students (i.e with class/level attached)
		* Each course/subject will also have the time table. 
		* Teachers will also have access to the PTA section under the Management Bay

	* School Admins 
		* They will responsible for creating the users. (Hopefully we can have a bulk upload feature to aid in adding multiple users at a go)
		* They will also be responsible for managing the school's content. Uploading the schools's time table, news about the school, event dates, etc. 
		* They will have a general oversight management of their organization's account 

	* Parents
		* Parents will be linked to their wards. 
		* They will only have access to the records of their wards, exams report, test scores, teacher's remarks
		* Parents will also have access to the PTA section under the Management Bay 


Features
	* Directories 
		* Online Class 
			* This feature enables students to have lessons online with their Teacher/tutor. The implementation will be a group video chat, where student can connect and the teacher can present using his video camera. 
			* Students will be able to ask questions under the lesson. 

		* Text Books 
			* Textbooks are under a subject/course. (Since the course is already under a class). This means even if there is the same book for multiple classes, it has to be added differently. 
			* Teachers will have access to upload soft copies of the books needed for their courses/subjects for students to download. 
			

		* Events
			* School events will be managed by the school admins. 
			* All users under the school will have access to see what events are upcoming.  
			* Only upcoming events will be shown. 

	* Management Bay 
		* Student's Record
			* Teachers will upload the records for the students enrolled in their subjects 
			* Parents will be able to see their students' records. 
			* Students will also be allowed to see their records. 

		* School Time Table 
			* Time Table will be uploaded by the school admin. This might also include important dates
			* Students will be allowed to see the Time Table 
			* The School Admin will upload the time table for the school. This is available to everyone. 
		* PTA Information 
			* The School Administrator will be responsible to uploading the PTA information of the school. 
			* The Parents will have a suggestion box to send their suggestions to the PTA. 
			* Minutes from previous PTA Meetings will be available here. 