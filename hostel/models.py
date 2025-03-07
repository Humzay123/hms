from django.contrib import admin
from django.db import models
from django.core.mail import send_mail
#from sqlalchemy import null

# Create your models here.
class RoomType(models.Model):
    name = models.CharField("type", max_length=200)

    class Meta:
        verbose_name_plural = "Room Type"

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField("Room No.",max_length=200)
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    description = models.CharField("description",max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Room"

    def __str__(self):
        return self.name


class Bed(models.Model):
    name = models.CharField("Bed No.",max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default='1')

    class Meta:
        verbose_name_plural = "Bed"

    def __str__(self):
        return self.name


class FeeType(models.Model):
    name = models.CharField("fee Type", max_length=200)
    duedate = models.DateField("due date")

    class Meta:
        verbose_name_plural = "Fee Type"
        ordering = ['-id']

    def __str__(self):
        return self.name


class FeeGroup(models.Model):
    name = models.CharField("fee Group", max_length=200)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Fee Group"

    def __str__(self):
        return self.name + " | " + str(self.amount)


# class FeeMaster(models.Model):
#     feegroup = models.ForeignKey(FeeGroup, on_delete=models.CASCADE, null=False, blank=False)
#     feetype = models.ForeignKey(FeeType, on_delete=models.CASCADE, null=False, blank=False)
#     duedate = models.DateField()
#     amount = models.PositiveIntegerField()

#     class Meta:
#         verbose_name_plural = "Fee Master"

#     @admin.display(ordering='feegroup')

#     def __str__(self):
#         return self.feegroup.name


class Boarder(models.Model):
    Living_Purpose = [
        ('Study', 'Study'),
        ('Job', 'Job'),
        ]

    Blood_Group = [
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
        ]

    Status = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    	]

    name = models.CharField("name",max_length=200)
    father_name = models.CharField("father Name",max_length=200)
    cell_no = models.CharField("cell No",max_length=200)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to ='students_pics/', blank=True, null=True)
    address = models.CharField("address",max_length=500)
    emergency_cell_no = models.CharField("Emergency Cell No", max_length=200)
    living_purpose = models.CharField("living Purpose" ,max_length=20, choices=Living_Purpose, default='Study')
    admission_date = models.DateField("admission Date", null=True, blank=True,)
    blood_group = models.CharField("blood Group", max_length=20, choices=Blood_Group)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, null=True, blank=True, related_name='all_beds')
    feegroup = models.ForeignKey(FeeGroup, on_delete=models.CASCADE, null=True, blank=False)
    notes = models.CharField("notes",max_length=200, blank=True)
    status = models.CharField("status", max_length=20, choices=Status, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('viewboarder', kwargs={'pk' : self.pk})

    def save(self, *args, **kwargs):
        new_student = not self.pk
        # Call the real save method
        super().save(*args, **kwargs)

        if new_student:
            # Send email to student after saving the model
            subject = "Admission Confirmation"
            message = "Dear " + self.name + ",\n\n"
            message += "We welcome you in this hostel and thank you for selecting us to serve you. In case, you have any queries feel free to contact us.\n\n"
            message += "Best regards,\nAdmin\nRoyal Boys Hostel"
            send_mail(subject, message, 'Royal Boys Hostel', [self.email], fail_silently=False)

    class Meta:
        verbose_name_plural = "Boarder"

    def __str__(self):
        return str(str(self.name) + " (" + str(self.bed) + ")")


class CollectFee(models.Model):
    boarder = models.ForeignKey(Boarder, on_delete=models.CASCADE)
    feetype = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amountdue = models.PositiveIntegerField("amount Due")
    amountpaid = models.PositiveIntegerField("amount Paid")
    balance = models.PositiveIntegerField("Balance")
    datepaid = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        new_student = not self.pk
        # Call the real save method
        super().save(*args, **kwargs)

        if new_student:
            # Send email to student after saving the model
            subject = "Fee Paid"
            message = "Dear " + self.boarder.name + ",\n\n"
            message += "You have successfully paid the fee against the fee type: {}\n\nAmount Due: {}\n\nAmount Paid: {}\n\nRemaining Amount: {}\n\nIn case you have any queries, feel free to contact us.\n\n".format(str(self.feetype), self.amountdue, self.amountpaid, self.balance)

            message += "Best regards,\nAdmin\nRoyal Boys Hostel"
            send_mail(subject, message, 'Royal Boys Hostel', [self.boarder.email], fail_silently=False)

    class Meta:
        verbose_name_plural = "Collect Fee"

    def __str__(self):
        return self.boarder.name


class IncomeHead(models.Model):
    name = models.CharField("income Head", max_length=200)
    description = models.CharField("description",max_length=1000)

    class Meta:
        verbose_name_plural = "Income Head"

    def __str__(self):
        return self.name

class Income(models.Model):
    incomehead = models.ForeignKey(IncomeHead, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField("name", max_length=200)
    invoiceno = models.CharField("invoice No", max_length=200)
    date = models.DateField()
    amount = models.PositiveIntegerField(null=True, blank=False)
    description = models.CharField("description",max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Income"

    def __str__(self):
        return self.name


class ExpenseHead(models.Model):
    name = models.CharField("expensce Head", max_length=200)
    description = models.CharField("description",max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Expense Head"

    def __str__(self):
        return self.name

class Expense(models.Model):
    expensehead = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField("name", max_length=200)
    invoiceno = models.CharField("invoice No", max_length=200)
    date = models.DateField()
    amount = models.PositiveIntegerField(null=True, blank=False)
    description = models.CharField("description",max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Expense"

    def __str__(self):
        return self.name

class LeaveNotice(models.Model):
    boarder = models.ForeignKey(Boarder, on_delete=models.CASCADE)
    leavingdate = models.DateField()
    description = models.CharField("description",max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Leaving Notice"

    def __str__(self):
        return self.boarder.name


class TodoList(models.Model):
    Status = [
        ('Pending', 'Pending'),
        ('Inprocess', 'Inprocess'),
        ('Completed', 'Completed'),
    	]

    description = models.CharField("description",max_length=1000)
    duedate = models.DateField()
    status = models.CharField("status", max_length=20, choices=Status, default='Pending')

    class Meta:
        verbose_name_plural = "Todo List"

    def __str__(self):
        return self.description


class ComplainType(models.Model):
    name = models.CharField("complain Type", max_length=200)

    class Meta:
        verbose_name_plural = "Complain Type"

    def __str__(self):
        return self.name

class Complain(models.Model):
    Status = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved')
        ]

    complaintype = models.ForeignKey(ComplainType, on_delete=models.CASCADE, default='1')
    description = models.CharField("description",max_length=1000)
    status = models.CharField("status", max_length=20, choices=Status, default='Pending')

    class Meta:
        verbose_name_plural = "Complain"

    def __str__(self):
        return self.description
