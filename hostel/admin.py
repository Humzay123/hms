from django.contrib import admin
from hostel.models import *

# Register your models here.
class BoarderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Boarder, BoarderAdmin)

class BedInline(admin.TabularInline):
    model = Bed

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        BedInline,
    ]
admin.site.register(Room, RoomAdmin)

class RoomInline(admin.TabularInline):
    model = Room

class RoomTypeAdmin(admin.ModelAdmin):
    inlines = [
        RoomInline,
    ]
admin.site.register(RoomType, RoomTypeAdmin)

class BedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bed, BedAdmin)

class FeeGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeeGroup, FeeGroupAdmin)

class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duedate')
admin.site.register(FeeType, FeeTypeAdmin)

class CollectFeeAdmin(admin.ModelAdmin):
    list_display = ('boarder', 'amountpaid')
admin.site.register(CollectFee, CollectFeeAdmin)

class IncomeHeadAdmin(admin.ModelAdmin):
    pass
admin.site.register(IncomeHead, IncomeHeadAdmin)

class IncomeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Income, IncomeAdmin)

class ExpenseHeadAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExpenseHead, ExpenseHeadAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Expense, ExpenseAdmin)

class LeaveNoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(LeaveNotice, LeaveNoticeAdmin)

class TodoListAdmin(admin.ModelAdmin):
    pass
admin.site.register(TodoList, TodoListAdmin)

class ComplainTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ComplainType, ComplainTypeAdmin)

class ComplainAdmin(admin.ModelAdmin):
    pass
admin.site.register(Complain, ComplainAdmin)
