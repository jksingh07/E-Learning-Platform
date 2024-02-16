# models.py

# Author: Jaskaran Singh Luthra
# Last Updated: 15-02-2024
# File Details: 
#   This file contains the models for the E-Learning Platform.
#   It implements the MVC (Model-View-Controller) architecture, where this file serves as the Model component.
#   The models define the structure of the database tables and their relationships.
#   The models defined in this file include User, Student, Faculty, Department, Course, Payment, Announcement, 
#   Assignment, Submission, Material, and Membership.

# ----------------------------------------------------------------------------------------------------------------------------
# Importing necessary modules and libraries
from django.db import models
from froala_editor.fields import FroalaField

# ----------------------------------------------------------------------------------------------------------------------------
# USER MODEL 
#   Model representing a user in the system. 
#   Users can be of two types: "Student" or "Faculty".
#   It stores basic information such as username, password, email, full name, and user type.
# ----------------------------------------------------------------------------------------------------------------------------
class User(models.Model):
    """
    Model representing a user in the system.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        full_name (str): The full name of the user.
        user_type (str): The type of user ('ST' for Student, 'FA' for Faculty).
    """
    # Choices for user types
    STUDENT = 'ST'   # 'ST' is abbreviation reffered in DB as Student
    FACULTY = 'FA'   # 'FA' is abbreviation reffered in DB as Student
    USER_TYPES = [
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
    ]

    # Fields for a User Object
    username = models.CharField(max_length=50, unique=True)  # Username is Unique
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True) # Email ID Should be Unique
    full_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=2, choices=USER_TYPES) # Choices = USER_TYPE, which gives 2 options 'ST' or 'FA', This is useful while sign up 

    def __str__(self) -> str:
        return self.username
# ----------------------------------------------------------------------------------------------------------------------------
    



# ----------------------------------------------------------------------------------------------------------------------------
# STUDENT MODEL
#   Model representing a student in the system. 
#   It contains information about a student including student ID, name, email, password, membership level, 
#   enrolled courses, profile picture, and department.
# ----------------------------------------------------------------------------------------------------------------------------
class Student(models.Model):
    """
    Model representing a student in the system.

    Attributes:
        student_id (int): The unique identifier for the student.
        name (str): The name of the student.
        email (str): The email address of the student.
        password (str): The password of the student.
        membership (str): The membership level of the student ('b' for Bronze, 's' for Silver, 'g' for Gold).
        role (str): The role of the student.
        course (ManyToManyField): The courses associated with the student.
        photo (ImageField): The profile picture of the student.
        department (ForeignKey): The department the student belongs to.
    """

    # Fields for Student Object
    student_id = models.IntegerField(primary_key=True)  # Student ID is the primary key (all IDs are Unique) in the DB, to prevent duplication  
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    MEMBERSHIP_CHOICES = (
        ('b', 'Bronze'),
        ('s', 'Silver'),
        ('g', 'Gold'),
    )

    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, blank=True, default='b')
   
    role = models.CharField(
        default="Student", max_length=100, null=False, blank=True)
    course = models.ManyToManyField(
        'Course', related_name='students', blank=True)
   
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_student.png')
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, blank=False, related_name='students')

    def delete(self, *args, **kwargs) -> None:
        """
        Override the delete method to remove associated photo if it's not default.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'


    def __str__(self) -> str:
        return self.name
# ----------------------------------------------------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------------------------------------------------
# FACULTY MODEL
#   Model representing a faculty member in the system. 
#   It stores details about a faculty member such as faculty ID, name, email, password, department, role, and profile picture.
# -----------------------------------------------------------------------------------------------------------------------------
class Faculty(models.Model):
    """
    Model representing a faculty member in the system.

    Attributes:
        faculty_id (int): The unique identifier for the faculty member.
        name (str): The name of the faculty member.
        email (str): The email address of the faculty member.
        password (str): The password of the faculty member.
        department (ForeignKey): The department the faculty member belongs to.
        role (str): The role of the faculty member.
        photo (ImageField): The profile picture of the faculty member.
    """
    faculty_id = models.IntegerField(primary_key=True) # Unique identifier for the faculty member
    name = models.CharField(max_length=100, null=False) # Name of the faculty member
    email = models.EmailField(max_length=100, null=True, blank=True)  # Email address of the faculty member
    password = models.CharField(max_length=255, null=False) # Password of the faculty member
    # Department of the faculty member, takes Department names from the Department table using faculty ID
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, related_name='faculty') 
    role = models.CharField(
        default="Faculty", max_length=100, null=False, blank=True) # Role of the faculty member,
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_faculty.png') # Profile Picture of the faculty member,

    def delete(self, *args, **kwargs) -> None:
        """
        Override the delete method to remove associated photo if it's not default.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.photo != 'profile_pics/default_faculty.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self) -> str:
        return self.name
# ----------------------------------------------------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------------------------------------------------
# DEPARTMENT MODEL
#   Model representing a department in the system. 
#   It contains information about a department including department ID, name, and description.
# ----------------------------------------------------------------------------------------------------------------------------
class Department(models.Model):
    """
    Model representing a department in the system.

    Attributes:
        department_id (int): The unique identifier for the department.
        name (str): The name of the department.
        description (str): The description of the department.
    """
    department_id = models.IntegerField(primary_key=True) # Depaertment ID is the primary key for Department Table in DB
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self) -> str:
        return self.name

    def student_count(self) -> int:
        """
        Get the count of students belonging to the department.

        Returns:
            int: The count of students.
        """
        return self.students.count()

    def faculty_count(self) -> int:
        """
        Get the count of faculty members belonging to the department.

        Returns:
            int: The count of faculty members.
        """
        return self.faculty.count()

    def course_count(self) -> int:
        """
        Get the count of courses belonging to the department.

        Returns:
            int: The count of courses.
        """
        return self.courses.count()
# ----------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------------
# COURSE MODEL
#   Model representing a course in the system. 
#   It stores details about a course such as course code, name, price, description, membership level, department, 
#   assigned faculty, and associated students.
# ----------------------------------------------------------------------------------------------------------------------------
class Course(models.Model):
    """
    Model representing a course in the system.

    Attributes:
        code (int): The unique identifier for the course.
        name (str): The name of the course.
        price (int): The price of the course.
        description (str): The description of the course.
        membership_level (str): The membership level of the course.
        department (ForeignKey): The department offering the course.
        faculty (ForeignKey): The faculty member teaching the course.
        studentKey (int): Unique identifier for the student.
        facultyKey (int): Unique identifier for the faculty member.
    """
    code = models.IntegerField(primary_key=True) # Unique Course code
    name = models.CharField(max_length=255, null=False, unique=True)
    price = models.IntegerField(default=100)
    description = models.CharField(max_length=200, default='Course Description')
    MEMBERSHIP_CHOICES = (
        ('b', 'Bronze'),
        ('s', 'Silver'),
        ('g', 'Gold'),
    )

    membership_level = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, related_name='courses')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    studentKey = models.IntegerField(null=False, unique=True)
    facultyKey = models.IntegerField(null=False, unique=True)

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name
# ----------------------------------------------------------------------------------------------------------------------------
    
# ----------------------------------------------------------------------------------------------------------------------------   
# PAYMENT MODEL
#   Model representing a payment transaction in the system. 
#   It contains information about a payment including the course for which payment is made, amount, description, and timestamp.
# ----------------------------------------------------------------------------------------------------------------------------
class Payment(models.Model):
    """
    Model representing a payment for a course.

    Attributes:
        course (ForeignKey): The course for which the payment is made.
        amount (Decimal): The amount of the payment.
        description (str): The description of the payment.
        timestamp (DateTime): The timestamp of the payment.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # Course for which the payment is made
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Amount of the payment
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True) # Timestamp of the payment

    def __str__(self) -> str:
        return f"Payment - {self.id}"

    def save(self, *args, **kwargs) -> None:
        """
        Override the save method to set the amount based on the course price.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.amount = self.course.price
        super(Payment, self).save(*args, **kwargs)
# ----------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------------
# ANNOUNCEMENT MODEL
#   Model representing an announcement in the system. 
#   It stores information about an announcement including the course to which it belongs, datetime of the announcement, and description.
# ----------------------------------------------------------------------------------------------------------------------------
class Announcement(models.Model):
    """
    Model representing an announcement for a course.

    Attributes:
        course_code (ForeignKey): The course for which the announcement is made.
        datetime (DateTime): The date and time of the announcement.
        description (FroalaField): The description of the announcement.
    """
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False) # Course associated with the announcement
    datetime = models.DateTimeField(auto_now_add=True, null=False) # Datetime of the announcement
    description = FroalaField()

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self) -> str:
        return self.datetime.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"


    def post_date(self) -> str:
        """
        Get the formatted date of the announcement.

        Returns:
            str: The formatted date string.
        """
        return self.datetime.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"

# ----------------------------------------------------------------------------------------------------------------------------
    


# ----------------------------------------------------------------------------------------------------------------------------
# ASSIGNMENT MODEL
#   Model representing an assignment in the system. 
#   It contains details about an assignment including the course to which it belongs, title, description, datetime of 
#   creation, deadline, attached file, and marks.
# ----------------------------------------------------------------------------------------------------------------------------
class Assignment(models.Model):
    """
    Model representing an assignment for a course.

    Attributes:
        course_code (ForeignKey): The course for which the assignment is assigned.
        title (str): The title of the assignment.
        description (str): The description of the assignment.
        datetime (DateTime): The date and time the assignment was created.
        deadline (DateTime): The deadline for the assignment.
        file (FileField): The file attached to the assignment.
        marks (Decimal): The maximum marks for the assignment.
    """
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False) # Course associated with the assignment
    title = models.CharField(max_length=255, null=False) # Title of the assignment
    description = models.TextField(null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True) # File attached to the assignment
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False) # Marks assigned to the assignment

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['-datetime']

    def __str__(self) -> str:
        return self.title

    def delete(self, *args, **kwargs) -> None:
        """
        Override the delete method to remove associated file.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self) -> str:
        """
        Get the formatted date of the assignment.

        Returns:
            str: The formatted date string.
        """
        return self.datetime.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"

    def due_date(self) -> str:
        """
        Get the formatted deadline of the assignment.

        Returns:
            str: The formatted deadline string.
        """
        return self.deadline.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"
# ----------------------------------------------------------------------------------------------------------------------------
    


# ----------------------------------------------------------------------------------------------------------------------------
# SUBMISSION MODEL
#   Model representing a submission of an assignment by a student in the system. 
#   It stores information about a submission including the assignment, student, submitted file, datetime of submission,
#   marks obtained, and status.
# ----------------------------------------------------------------------------------------------------------------------------
class Submission(models.Model):
    """
    Model representing a submission for an assignment.

    Attributes:
        assignment (ForeignKey): The assignment for which the submission is made.
        student (ForeignKey): The student who made the submission.
        file (FileField): The file attached to the submission.
        datetime (DateTime): The date and time the submission was made.
        marks (Decimal): The marks obtained for the submission.
        status (str): The status of the submission.
    """
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False) # Assignment associated with the submission
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False) # Student who submitted the assignment
    file = models.FileField(upload_to='submissions/', null=True,) # File submitted for the assignment
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True) # Status of the submission

    def file_name(self) -> str:
        """
        Get the name of the submitted file.

        Returns:
            str: The name of the file.
        """
        return self.file.name.split('/')[-1]

    def time_difference(self) -> str:
        """
        Get the difference between submission and deadline.

        Returns:
            str: The formatted time difference string.
        """
        difference = self.assignment.deadline - self.datetime
        days = difference.days
        hours = difference.seconds//3600
        minutes = (difference.seconds//60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " seconds"
                else:
                    return str(minutes) + " minutes " + str(seconds) + " seconds"
            else:
                return str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            return str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

    def submission_date(self) -> str:
        """
        Get the formatted date of the submission.

        Returns:
            str: The formatted date string.
        """
        return self.datetime.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"


    def delete(self, *args, **kwargs) -> None:
        """
        Override the delete method to remove associated file.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['datetime']
# ----------------------------------------------------------------------------------------------------------------------------
        



# ----------------------------------------------------------------------------------------------------------------------------
# MATERIAL MODEL
#   Model representing study materials in the system. 
#   It contains details about study materials including the course to which it belongs, description, datetime of creation, and attached file.
# ----------------------------------------------------------------------------------------------------------------------------
class Material(models.Model):
    """
    Model representing study materials for a course.

    Attributes:
        course_code (ForeignKey): The course for which the material is provided.
        description (str): The description of the material.
        datetime (DateTime): The date and time the material was uploaded.
        file (FileField): The file attached to the material.
    """
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False) # Course associated with the material
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    file = models.FileField(upload_to='materials/', null=True, blank=True) # File attached to the material

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']

    def __str__(self) -> str:
        return self.title

    def delete(self, *args, **kwargs) -> None:
        """
        Override the delete method to remove associated file.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self) -> str:
        """
        Get the formatted date of the material.

        Returns:
            str: The formatted date string.
        """
        return self.datetime.strftime("%d-%b-%y, %I:%M %p") #Formats the deadline datetime object as a string in the format "day-month-year, hour:minute AM/PM"

# ----------------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------------------------------
# MEMBERSHIP MODEL
#   Model representing a membership plan in the system. 
#   It stores information about a membership plan including name, price, and features.
# ----------------------------------------------------------------------------------------------------------------------------
class Membership(models.Model):
    """
    Model representing a membership level.

    Attributes:
        name (str): The name of the membership level.
        price (Decimal): The price of the membership level.
        features (str): The features included in the membership level.
    """
    name = models.CharField(max_length=100) # Name of the membership plan
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    features = models.TextField() # Features offered by the membership plan

    def __str__(self) -> str:
        return self.name
# ----------------------------------------------------------------------------------------------------------------------------