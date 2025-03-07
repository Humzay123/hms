from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from hostel.models import *
from hostel.forms import *
from django.db.models import Count, Sum, Q, Min, Max
from datetime import datetime
#For Login
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from hostel.decorators import unauthenticated_user

# Create your views here.
@login_required(login_url='loginpage')
def dashboard(request):
	boarders = Boarder.objects.all()
	no_of_boarders = boarders.count()

	beds = Bed.objects.all()
	no_of_beds = beds.count()
	alltodo = TodoList.objects.all().order_by('-id')

	aassigned_beds = Boarder.objects.filter(bed_id__isnull=False).count()

	available_beds = no_of_beds - aassigned_beds

	searchdatestart = "1999-01-01"
	searchdateend = "4000-01-01"

	if request.method=="POST":
		searchdatestart = request.POST.get('searchdatestart')
		searchdateend = request.POST.get('searchdateend')

	totalincomes = Income.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalincome=Sum('amount'))
	totalfeeincomes = CollectFee.objects.aggregate(totalfeeincome=Sum('amountpaid'))
	totalexpenses = Expense.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalexpense=Sum('amount'))

	context = {'no_of_boarders':no_of_boarders, 'no_of_beds':no_of_beds, 'aassigned_beds':aassigned_beds, 'available_beds':available_beds, 'alltodo':alltodo, 'totalincomes':totalincomes, 'totalfeeincomes':totalfeeincomes, 'totalexpenses':totalexpenses, 'dashmo':'menu-open', 'dashac':'active'}
	return render(request, 'dashboard.html', context)


# def newboarder(request):
# 	beds = Bed.objects.all()
# 	fee_groups = FeeGroup.objects.all()

# 	if request.method=="POST":
# 		newboarder = Boarder()
# 		name = request.POST.get('name')
# 		father_name = request.POST.get('father_name')
# 		cell_no = request.POST.get('cell_no')
# 		address = request.POST.get('address')
# 		emergency_cell_no = request.POST.get('emergency_cell_no')
# 		living_purpose = request.POST.get('living_purpose')
# 		blood_group = request.POST.get('blood_group')
# 		bed_id = request.POST.get('bed')
# 		feegroup_id = request.POST.get('feegroup')
# 		notes = request.POST.get('notes')
# 		status = request.POST.get('status')

# 		newboarder.name=name
# 		newboarder.father_name=father_name
# 		newboarder.cell_no=cell_no
# 		newboarder.address=address
# 		newboarder.emergency_cell_no=emergency_cell_no
# 		newboarder.living_purpose=living_purpose
# 		newboarder.blood_group=blood_group
# 		newboarder.bed_id=bed_id
# 		newboarder.feegroup_id=feegroup_id
# 		newboarder.notes=notes
# 		newboarder.status=status

# 		if len(request.FILES) != 0:
# 			newboarder.photo = request.FILES['photo']

# 		newboarder.save()
# 		messages.success(request, newboarder.name)
# 		return redirect('/newboarder')
# 	context = {'beds':beds, 'fee_groups':fee_groups}
# 	return render(request, 'new-boarder.html', context)


@login_required(login_url='loginpage')
def newboarder(request):
	form = BoarderForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "New boarder added successfully.")
		return redirect('/newboarder')

	context = {'title':"New Boarder", 'header_title':"Add New Boarder", 'bormo': 'menu-open', 'naborac': 'active', 'nborac':'active' ,'form':form}
	return render(request, 'new-boarder.html', context)


@login_required(login_url='loginpage')
def allboardersinformation(request):
	boarders = Boarder.objects.all()
	context = {'boarders':boarders, 'bormo': 'menu-open', 'naborac': 'active', 'aborac':'active'}
	return render(request, 'allboarders-information.html', context)


@login_required(login_url='loginpage')
def viewboarder(request, id):
	boarder = get_object_or_404(Boarder, pk=id)

	fee_by_student = CollectFee.objects.filter(boarder_id=id)
	
	context = {'boarder':boarder, 'fee_by_student':fee_by_student, 'bormo': 'menu-open', 'naborac': 'active', 'aborac':'active'}
	return render(request, 'view-boarder.html', context)


@login_required(login_url='loginpage')
def updateboarder(request,id):
	boarder = Boarder.objects.get(pk=id)

	def create_form(request, boarder):

		class BoarderForm(forms.ModelForm):
			class Meta:
				model = Boarder
				fields = ['name', 'father_name', 'cell_no', 'photo', 'address', 'emergency_cell_no', 'living_purpose', 'admission_date', 'blood_group', 'bed', 'feegroup', 'notes', 'status']

				widgets = {
            		'name': forms.TextInput(attrs={'class': 'form-control'}),
            		'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            		'cell_no': forms.TextInput(attrs={'class': 'form-control'}),
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
				self.fields['bed'].queryset = Bed.objects.filter(Q(all_beds__bed__isnull=True)|Q(all_beds__id=boarder.id))

		return BoarderForm

	BoarderForm = create_form(request, boarder)

	if request.method == 'POST':
		form = BoarderForm(request.POST, instance=boarder)
		if form.is_valid():
			form.save()
			messages.success(request, "Boarder updated successfully.")
			return redirect('/boarder/view/'+id)
	else:
		form = BoarderForm(instance=boarder)
		context= {'title':"Update Boarder", 'header_title':"Update Boarder's Details", 'form':form, 'bormo': 'menu-open', 'naborac': 'active', 'aborac':'active'}
		return render(request, 'new-boarder.html', context)


@login_required(login_url='loginpage')
def deleteboarder(request, id):
	boarder = get_object_or_404(Boarder, pk=id)
	boarder.delete()
	messages.success(request, "Boarder deleted successfully.")
	return HttpResponseRedirect(reverse('allboardersinformation'))


# def updateboarder(request,id):
#     boarder = Boarder.objects.get(pk=id)
#     form = BoarderForm(instance=boarder)
#     if request.method == 'POST':
#         form = BoarderForm(request.POST, instance=boarder)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Boarder updated successfully.")
#             return redirect('/boarder/view/'+id)

#     context= {'title':"Update Boarder", 'header_title':"Update Boarder's Details", 'form':form}
#     return render(request, 'new-boarder.html', context)


@login_required(login_url='loginpage')
def roomtype(request):
	allroomtypes = RoomType.objects.all()

	form = RoomTypeForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Room type added successfully.")
		return redirect('/roomtype')
	context = {'allroomtypes':allroomtypes, 'roomtype':'Add Room Type', 'roomtypes':'Room Types', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'rootac':'active'}
	return render(request, 'room-type.html', context)


@login_required(login_url='loginpage')
def updateroomtype(request,id):
	allroomtypes = RoomType.objects.all()

	roomtype = RoomType.objects.get(pk=id)

	form = RoomTypeForm(instance=roomtype)
	if request.method == 'POST':
		form = RoomTypeForm(request.POST, instance=roomtype)
		if form.is_valid():
			form.save()
			messages.success(request, "Room type updated successfully.")
			return redirect('/roomtype')

	context= {'allroomtypes':allroomtypes, 'roomtype':'Add Room Type', 'roomtypes':'Room Types', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'rootac':'active'}
	return render(request, 'room-type.html', context)


@login_required(login_url='loginpage')
def deleteroomtype(request, id):
	roomtype = get_object_or_404(RoomType, pk=id)
	roomtype.delete()
	messages.success(request, "Room Type deleted successfully.")
	return HttpResponseRedirect(reverse('roomtype'))


@login_required(login_url='loginpage')
def room(request):
	allrooms = Room.objects.all()

	total_beds = Bed.objects.all().annotate(num_beds=Count("all_beds"))
	assigned_beds = total_beds.filter(num_beds__gt=0)
	unassigned_beds = total_beds.exclude(num_beds__gt=0)

	form = RoomForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Room added successfully.")
		return redirect('/room')
	context = {'allrooms':allrooms, 'unassigned_beds':unassigned_beds, 'room':'Add Room', 'rooms':'Rooms', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'rooac':'active'}
	return render(request, 'room.html', context)


@login_required(login_url='loginpage')
def updateroom(request,id):
	allrooms = Room.objects.all()

	room = Room.objects.get(pk=id)

	form = RoomForm(instance=room)
	if request.method == 'POST':
		form = RoomForm(request.POST, instance=room)
		if form.is_valid():
			form.save()
			messages.success(request, "Room updated successfully.")
			return redirect('/room')

	context= {'allrooms':allrooms, 'room':'Add Room', 'rooms':'Rooms', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'rooac':'active'}
	return render(request, 'room.html', context)


@login_required(login_url='loginpage')
def deleteroom(request, id):
	room = get_object_or_404(Room, pk=id)
	room.delete()
	messages.success(request, "Room deleted successfully.")
	return HttpResponseRedirect(reverse('room'))


@login_required(login_url='loginpage')
def bed(request):
	allbeds = Bed.objects.all()

	total_beds = Bed.objects.all().annotate(num_beds=Count("all_beds"))
	assigned_beds = total_beds.filter(num_beds__gt=0)
	unassigned_beds = total_beds.exclude(num_beds__gt=0)

	form = BedForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Bed added successfully.")
		return redirect('/bed')
	context = {'allbeds':allbeds, 'assigned_beds':assigned_beds, 'bed':'Add Bed', 'beds':'Beds', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'bedac':'active'}
	return render(request, 'bed.html', context)


@login_required(login_url='loginpage')
def updatebed(request,id):
	allbeds = Bed.objects.all()

	bed = Bed.objects.get(pk=id)

	total_beds = Bed.objects.all().annotate(num_beds=Count("all_beds"))
	assigned_beds = total_beds.filter(num_beds__gt=0)

	form = BedForm(instance=bed)
	if request.method == 'POST':
		form = BedForm(request.POST, instance=bed)
		if form.is_valid():
			form.save()
			messages.success(request, "Bed updated successfully.")
			return redirect('/bed')

	context= {'allbeds':allbeds, 'assigned_beds':assigned_beds, 'bed':'Add Bed', 'beds':'Beds', 'form':form, 'roommo':'menu-open', 'roomac':'active', 'bedac':'active'}
	return render(request, 'bed.html', context)


@login_required(login_url='loginpage')
def deletebed(request, id):
	bed = get_object_or_404(Bed, pk=id)
	bed.delete()
	messages.success(request, "Bed deleted successfully.")
	return HttpResponseRedirect(reverse('bed'))


@login_required(login_url='loginpage')
def feetype(request):
	allfeetypes = FeeType.objects.all()

	form = FeeTypeForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Fee Type added successfully.")
		return redirect('/feetype')
	context = {'allfeetypes':allfeetypes, 'feetype':'Add Fee Type', 'feetypes':'Fee Type', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feetac':'active'}
	return render(request, 'feetype.html', context)


@login_required(login_url='loginpage')
def updatefeetype(request,id):
	allfeetypes = FeeType.objects.all()

	feetype = FeeType.objects.get(pk=id)

	form = FeeTypeForm(instance=feetype)
	if request.method == 'POST':
		form = FeeTypeForm(request.POST, instance=feetype)
		if form.is_valid():
			form.save()
			messages.success(request, "Fee type updated successfully.")
			return redirect('/feetype')

	context= {'allfeetypes':allfeetypes, 'feetype':'Add Fee Type', 'feetypes':'Fee Types', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feeac':'active'}
	return render(request, 'feetype.html', context)


@login_required(login_url='loginpage')
def deletefeetype(request, id):
	feetype = get_object_or_404(FeeType, pk=id)
	feetype.delete()
	messages.success(request, "Fee Type deleted successfully.")
	return HttpResponseRedirect(reverse('feetype'))


@login_required(login_url='loginpage')
def feegroup(request):
	allfeegroups = FeeGroup.objects.all()

	form = FeeGroupForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Fee Group added successfully.")
		return redirect('/feegroup')
	context = {'allfeegroups':allfeegroups, 'feegroup':'Add Fee Group', 'feegroups':'Fee Groups', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feegac':'active'}
	return render(request, 'feegroup.html', context)


@login_required(login_url='loginpage')
def updatefeegroup(request,id):
	allfeegroups = FeeGroup.objects.all()

	feegroup = FeeGroup.objects.get(pk=id)

	form = FeeGroupForm(instance=feegroup)
	if request.method == 'POST':
		form = FeeGroupForm(request.POST, instance=feegroup)
		if form.is_valid():
			form.save()
			messages.success(request, "Fee group updated successfully.")
			return redirect('/feegroup')

	context= {'allfeegroups':allfeegroups, 'feegroup':'Add Fee Group', 'feegroups':'Fee Groups', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feegac':'active'}
	return render(request, 'feegroup.html', context)


@login_required(login_url='loginpage')
def deletefeegroup(request, id):
	feegroup = get_object_or_404(FeeGroup, pk=id)
	feegroup.delete()
	messages.success(request, "Fee Group deleted successfully.")
	return HttpResponseRedirect(reverse('feegroup'))


@login_required(login_url='loginpage')
def feecollection(request):
	boarders = Boarder.objects.all()
	context = {'boarders':boarders, 'feemo':'menu-open', 'feeac':'active', 'feecac':'active'}
	return render(request, 'feecollection.html', context)


@login_required(login_url='loginpage')
def collectfee(request,id):
	boarder = Boarder.objects.get(pk=id)

	form = CollectFeeForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, "Fee added successfully.")
			return redirect('/boarders')

	fee_by_student = CollectFee.objects.filter(boarder_id=id).order_by('-id')

	context= {'boarder':boarder, 'fee_by_student':fee_by_student, 'collectfee':'Collect Fee', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feecac':'active'}
	return render(request, 'collectfee.html', context)


@login_required(login_url='loginpage')
def updatecollectfee(request,id):
	collectfee = CollectFee.objects.get(pk=id)

	form = CollectFeeForm(instance=collectfee)
	if request.method == 'POST':
		form = CollectFeeForm(request.POST, instance=collectfee)
		if form.is_valid():
			form.save()
			messages.success(request, "Fee updated successfully.")
			return redirect('/boarders')

	context= {'collectfee':collectfee,'updatefee':'Update Fee', 'form':form, 'feemo':'menu-open', 'feeac':'active', 'feecac':'active'}
	return render(request, 'collectfee.html', context)


@login_required(login_url='loginpage')
def deletecollectfee(request, id):
	collectfee = get_object_or_404(CollectFee, pk=id)
	collectfee.delete()
	messages.success(request, "Fee deleted successfully.")
	return HttpResponseRedirect(reverse('allboardersinformation'))


@login_required(login_url='loginpage')
def feedue(request):
	latest_feetype = FeeType.objects.all().aggregate(Max('duedate'))['duedate__max']
	boarders = Boarder.objects.filter(status='Active').exclude(collectfee__feetype__duedate=latest_feetype)
	context = {'boarders':boarders, 'feemo':'menu-open', 'feeac':'active', 'feedac':'active'}
	return render(request, 'fee-due.html', context)


@login_required(login_url='loginpage')
def expensehead(request):
	allexpenseheads = ExpenseHead.objects.all()

	form = ExpenseHeadForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Expense head added successfully.")
		return redirect('/expensehead')
	context = {'allexpenseheads':allexpenseheads, 'expensehead':'Add Expense Head', 'expenseheads':'Expense Heads', 'form':form, 'exmo':'menu-open', 'exac':'active', 'exhac':'active'}
	return render(request, 'expense-head.html', context)


@login_required(login_url='loginpage')
def updateexpensehead(request,id):
	allexpenseheads = ExpenseHead.objects.all()
	expensehead = ExpenseHead.objects.get(pk=id)

	form = ExpenseHeadForm(instance=expensehead)
	if request.method == 'POST':
		form = ExpenseHeadForm(request.POST, instance=expensehead)
		if form.is_valid():
			form.save()
			messages.success(request, "Expense head updated successfully.")
			return redirect('/expensehead')

	context= {'allexpenseheads':allexpenseheads, 'expensehead':'Add Ecpense Head', 'expenseheads':'Expense Heads', 'form':form,'exmo':'menu-open', 'exac':'active', 'exhac':'active'}
	return render(request, 'expense-head.html', context)


@login_required(login_url='loginpage')
def deleteexpensehead(request, id):
	expensehead = get_object_or_404(ExpenseHead, pk=id)
	expensehead.delete()
	messages.success(request, "Expense head deleted successfully.")
	return HttpResponseRedirect(reverse('expensehead'))


@login_required(login_url='loginpage')
def expense(request):
	allexpenses = Expense.objects.all()

	form = ExpenseForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Expense added successfully.")
		return redirect('/expense')
	context = {'allexpenses':allexpenses, 'expense':'Add Expense', 'expenses':'Expenses', 'form':form, 'exmo':'menu-open', 'exac':'active', 'aexac':'active'}
	return render(request, 'expense.html', context)


@login_required(login_url='loginpage')
def updateexpense(request,id):
	allexpenses = Expense.objects.all()

	expense = Expense.objects.get(pk=id)

	form = ExpenseForm(instance=expense)
	if request.method == 'POST':
		form = ExpenseForm(request.POST, instance=expense)
		if form.is_valid():
			form.save()
			messages.success(request, "Expense updated successfully.")
			return redirect('/expense')

	context= {'allexpenses':allexpenses, 'expense':'Expense', 'expenses':'Expenses', 'form':form, 'exmo':'menu-open', 'exac':'active', 'aexac':'active'}
	return render(request, 'expense.html', context)


@login_required(login_url='loginpage')
def deleteexpense(request, id):
	expense = get_object_or_404(Expense, pk=id)
	expense.delete()
	messages.success(request, "Expense deleted successfully.")
	return HttpResponseRedirect(reverse('expense'))


@login_required(login_url='loginpage')
def expensesearch(request):
	searchdatestart = "1999-01-01"
	searchdateend = "1999-01-01"

	if request.method=="POST":
		searchdatestart = request.POST.get('searchdatestart')
		searchdateend = request.POST.get('searchdateend')

	allexpenses = Expense.objects.filter(date__range=[searchdatestart, searchdateend])
	
	totalexpenses = Expense.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalexpense=Sum('amount'))

	context = {'allexpenses':allexpenses, 'totalexpenses':totalexpenses, 'expense':'Search Expense', 'expenses':'Expenses', 'exmo':'menu-open', 'exac':'active', 'sexac':'active'}

	return render(request, 'expense-search.html', context)


@login_required(login_url='loginpage')
def incomehead(request):
	allincomeheads = IncomeHead.objects.all()

	form = IncomeHeadForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Income head added successfully.")
		return redirect('/incomehead')
	context = {'allincomeheads':allincomeheads, 'incomehead':'Add Income Head', 'incomeheads':'Income Heads', 'form':form, 'inmo':'menu-open', 'inac':'active', 'inhac':'active'}
	return render(request, 'income-head.html', context)


@login_required(login_url='loginpage')
def updateincomehead(request,id):
	allincomeheads = IncomeHead.objects.all()

	incomehead = IncomeHead.objects.get(pk=id)

	form = IncomeHeadForm(instance=incomehead)
	if request.method == 'POST':
		form = IncomeHeadForm(request.POST, instance=incomehead)
		if form.is_valid():
			form.save()
			messages.success(request, "Income head updated successfully.")
			return redirect('/incomehead')

	context= {'allincomeheads':allincomeheads, 'incomehead':'Add Income Head', 'incomeheads':'Income Heads', 'form':form, 'inmo':'menu-open', 'inac':'active', 'inhac':'active'}
	return render(request, 'income-head.html', context)


@login_required(login_url='loginpage')
def deleteincomehead(request, id):
	incomehead = get_object_or_404(IncomeHead, pk=id)
	incomehead.delete()
	messages.success(request, "Income head deleted successfully.")
	return HttpResponseRedirect(reverse('incomehead'))


@login_required(login_url='loginpage')
def income(request):
	allincomes = Income.objects.all()

	form = IncomeForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		form.save()
		messages.success(request, "Income added successfully.")
		return redirect('/income')
	context = {'allincomes':allincomes, 'income':'Add Income', 'incomes':'Incomes', 'form':form, 'inmo':'menu-open', 'inac':'active', 'ainac':'active'}
	return render(request, 'income.html', context)


@login_required(login_url='loginpage')
def updateincome(request,id):
	allincomes = Income.objects.all()

	income = Income.objects.get(pk=id)

	form = IncomeForm(instance=income)
	if request.method == 'POST':
		form = IncomeForm(request.POST, instance=income)
		if form.is_valid():
			form.save()
			messages.success(request, "Income updated successfully.")
			return redirect('/income')

	context= {'allincomes':allincomes, 'income':'Income', 'incomes':'Incomes', 'form':form, 'inmo':'menu-open', 'inac':'active', 'ainac':'active'}
	return render(request, 'income.html', context)


@login_required(login_url='loginpage')
def deleteincome(request, id):
	income = get_object_or_404(Income, pk=id)
	income.delete()
	messages.success(request, "Income deleted successfully.")
	return HttpResponseRedirect(reverse('income'))


@login_required(login_url='loginpage')
def incomesearch(request):
	searchdatestart = "1999-01-01"
	searchdateend = "1999-01-01"

	if request.method=="POST":
		searchdatestart = request.POST.get('searchdatestart')
		searchdateend = request.POST.get('searchdateend')

	allincomes = Income.objects.filter(date__range=[searchdatestart, searchdateend])

	totalincomes = Income.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalincome=Sum('amount'))
	totalfeeincomes = CollectFee.objects.filter(datepaid__range=[searchdatestart, searchdateend]).aggregate(totalfeeincome=Sum('amountpaid'))

	context = {'allincomes':allincomes, 'totalincomes':totalincomes, 'totalfeeincomes':totalfeeincomes, 'income':'Search Income', 'incomes':'Incomes', 'inmo':'menu-open', 'inac':'active', 'sinac':'active'}

	return render(request, 'income-search.html', context)


@login_required(login_url='loginpage')
def profitsearch(request):
	searchdatestart = "1999-01-01"
	searchdateend = "1999-01-01"

	if request.method=="POST":
		searchdatestart = request.POST.get('searchdatestart')
		searchdateend = request.POST.get('searchdateend')

	totalincomes = Income.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalincome=Sum('amount'))
	totalfeeincomes = CollectFee.objects.filter(datepaid__range=[searchdatestart, searchdateend]).aggregate(totalfeeincome=Sum('amountpaid'))
	totalexpenses = Expense.objects.filter(date__range=[searchdatestart, searchdateend]).aggregate(totalexpense=Sum('amount'))

	context = {'totalincomes':totalincomes, 'totalfeeincomes':totalfeeincomes, 'totalexpenses':totalexpenses, 'searchprofit':'Search Profit', 'profit':'Profit', 'prmo':'menu-open', 'prac':'active', 'sinac':'active'}

	return render(request, 'profit-search.html', context)

@login_required(login_url='loginpage')
def leavenotice(request):
	allnotices = LeaveNotice.objects.all().exclude(boarder__status='Inactive')

	form = LeaveNoticeForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, "Leave notice added successfully.")
			return redirect('/leavenotice')
	context = {'form':form, 'allnotices':allnotices, 'notice':'Add Notice', 'notices':'Notices', 'lnmo':'menu-open', 'lnac':'active'}
	return render(request, 'leave-notice.html', context)


@login_required(login_url='loginpage')
def updateleavenotice(request,id):
	allnotices = LeaveNotice.objects.all()

	leavenotice = LeaveNotice.objects.get(pk=id)

	form = LeaveNoticeForm(instance=leavenotice)
	if request.method == 'POST':
		form = LeaveNoticeForm(request.POST, instance=leavenotice)
		if form.is_valid():
			form.save()
			messages.success(request, "Leave notice updated successfully.")
			return redirect('/leavenotice')

	context= {'form':form, 'allnotices':allnotices, 'notice':'Add Notice', 'notices':'Notices', 'lnmo':'menu-open', 'lnac':'active'}
	return render(request, 'leave-notice.html', context)


@login_required(login_url='loginpage')
def deleteleavenotice(request, id):
	leavenotice = get_object_or_404(LeaveNotice, pk=id)
	leavenotice.delete()
	messages.success(request, "Leave notice deleted successfully.")
	return HttpResponseRedirect(reverse('leavenotice'))


@login_required(login_url='loginpage')
def todolist(request):
	alltodo = TodoList.objects.all()

	form = TodoListForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			messages.success(request, "Task added successfully.")
			return redirect('/todolist')
	context = {'form':form, 'alltodo':alltodo, 'task':'Add Task', 'todolist':'Todo List', 'tdmo':'menu-open', 'tdac':'active'}
	return render(request, 'todo-list.html', context)


@login_required(login_url='loginpage')
def updatetodolist(request,id):
	alltodo = TodoList.objects.all()

	todo = TodoList.objects.get(pk=id)

	form = TodoListForm(instance=todo)
	if request.method == 'POST':
		form = TodoListForm(request.POST, instance=todo)
		if form.is_valid():
			form.save()
			messages.success(request, "Task updated successfully.")
			return redirect('/todolist')

	context = {'form':form, 'alltodo':alltodo, 'task':'Add Task', 'todolist':'Todo List', 'tdmo':'menu-open', 'tdac':'active'}
	return render(request, 'todo-list.html', context)


@login_required(login_url='loginpage')
def deletetodolist(request, id):
	todo = get_object_or_404(TodoList, pk=id)
	todo.delete()
	messages.success(request, "Task deleted successfully.")
	return HttpResponseRedirect(reverse('todolist'))


@login_required(login_url='loginpage')
def deletetodolistdashboard(request, id):
	todo = get_object_or_404(TodoList, pk=id)
	todo.delete()
	messages.success(request, "Task deleted successfully.")
	return HttpResponseRedirect(reverse('dashboard'))	

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('dashboard')

        else:
            messages.warning(request, "Username or Password is incorrect.")

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginpage')

# def updatestudent(request,id):
#     student = Student.objects.get(pk=id)
#     form = StudentForm(instance=student)
#     if request.method == 'POST':
#         #print('Printing Post:', request)
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Student updated successfully.")
#             return redirect('/student/view/'+id)

#     context= {'form':form}
#     return render(request, 'new-student.html', context)

@login_required(login_url='loginpage')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please ensure the password criteria.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', {
        'form': form
    })
