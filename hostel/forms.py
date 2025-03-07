from django import forms
from .models import *

class BoarderForm(forms.ModelForm):
    class Meta:
        model = Boarder
        fields = ['name', 'father_name', 'cell_no', 'email', 'photo', 'address', 'emergency_cell_no', 'living_purpose', 'admission_date', 'blood_group', 'bed', 'feegroup', 'notes', 'status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cell_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows' : 3}),
            'emergency_cell_no': forms.TextInput(attrs={'class': 'form-control'}),
            'living_purpose': forms.Select(attrs={'class': 'form-control select2'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#admission_date',}),
            'blood_group': forms.Select(attrs={'class': 'form-control select2'}),
            'bed': forms.Select(attrs={'class': 'form-control select2'}),
            'feegroup': forms.Select(attrs={'class': 'form-control select2'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows' : 3}),
            'status': forms.Select(attrs={'class': 'form-control select2'}),
         }

    def __init__(self, *args, **kwargs):
        super (BoarderForm, self).__init__(*args, **kwargs)
        self.fields['bed'].queryset = Bed.objects.filter(all_beds__bed__isnull=True)


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
         }


        labels = {
            'name': 'name:',
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'roomtype', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roomtype': forms.Select(attrs={'class': 'form-control select2'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['name', 'room']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control select2'}),
         }


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['name', 'duedate']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duedate': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#feetype',}),
         }


class FeeGroupForm(forms.ModelForm):
    class Meta:
        model = FeeGroup
        fields = ['name', 'amount']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
         }


class CollectFeeForm(forms.ModelForm):
    class Meta:
        model = CollectFee
        fields = ['boarder' ,'feetype', 'amountdue', 'amountpaid', 'balance']

        widgets = {
            'boarder': forms.Select(attrs={'class': 'form-control select2'}),
            'feetype': forms.Select(attrs={'class': 'form-control select2'}),
            'amountdue': forms.TextInput(attrs={'class': 'form-control'}),
            'amountpaid': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.TextInput(attrs={'class': 'form-control'}),
         }


# class FeeMasterForm(forms.ModelForm):
#     class Meta:
#         model = FeeMaster
#         fields = ['feegroup', 'feetype', 'duedate', 'amount']

#         widgets = {
#             'feegroup': forms.Select(attrs={'class': 'form-control'}),
#             'feetype': forms.Select(attrs={'class': 'form-control'}),
#             'duedate': forms.DateInput(attrs={'class': 'form-control'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control'}),
#          }


class ExpenseHeadForm(forms.ModelForm):
    class Meta:
        model = ExpenseHead
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expensehead', 'name', 'invoiceno', 'date', 'amount', 'description']

        widgets = {
            'expensehead': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'invoiceno': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#expense',}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class IncomeHeadForm(forms.ModelForm):
    class Meta:
        model = IncomeHead
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['incomehead', 'name', 'invoiceno', 'date', 'amount', 'description']

        widgets = {
            'incomehead': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'invoiceno': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#expense',}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class LeaveNoticeForm(forms.ModelForm):
    class Meta:
        model = LeaveNotice
        fields = ['boarder' ,'leavingdate', 'description']

        widgets = {
            'boarder': forms.Select(attrs={'class': 'form-control select2'}),
            'leavingdate': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#expense',}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
         }


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['description' ,'duedate', 'status']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'duedate': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#expense',}),
            'status': forms.Select(attrs={'class': 'form-control select2'}),
         }