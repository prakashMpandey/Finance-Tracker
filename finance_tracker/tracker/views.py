from django.shortcuts import render
from django.shortcuts import get_object_or_404,get_list_or_404,redirect
from .models import Transaction,Category
from .forms import TransactionForm
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import ExtractWeekDay
# Create your views here.
import calendar
from django.utils import timezone
from django.db.models import Sum, Q


@login_required
def create_transaction(request):
    if request.method=='POST':


        form=TransactionForm(request.POST)


        if form.is_valid():
            t_name=form.cleaned_data['transaction_name']
            amount=form.cleaned_data['amount']
            t_type=form.cleaned_data['transaction_Type']
            date=form.cleaned_data['date']
            

            category=form.cleaned_data['category']

            
            transaction=Transaction(t_name=t_name,amount=amount,type=t_type,
            category=category,user=request.user,date=date)
            transaction.save()
            return redirect("dashboard")
    else:
        form=TransactionForm()
    
    return render(request,"add_transaction.html",{"form":form})

@login_required
def get_transactions(request):

    trans=Transaction.objects.filter(user=request.user)
   
    if request.method=='POST':

        category=request.POST['category']
        month_filter=request.POST['month']

        if  category!=None and category!="0" :
            trans=trans.filter(category=category)

        if month_filter :
            year,month=month_filter.split("-")
            print(year,month)
            trans=trans.filter(date__year=year,date__month=month)


        print(request.POST,category)
        pass

    paginator=Paginator(trans,5)
    page=request.GET.get('page')
    finalData=paginator.get_page(page)
    categories=Category.objects.all();
   
    return render(request,"transactions.html",{"transactions":finalData,"categories":categories})

@login_required
def dashboard_data(request):

    # total_income=Transaction.objects.filter(type="income",user=request.user).aggregate()
    current_month=datetime.now().month
    total_expense=(Transaction.objects.filter(type='expense',user=request.user,date__month=current_month).aggregate(total=Sum('amount'))['total'] or Decimal(0))

    total_income=(Transaction.objects.filter(type='income',user=request.user,date__month=current_month).aggregate(total=Sum('amount'))['total'] or Decimal(0))

    balance = total_income-total_expense if total_income and total_expense else 0
    print(total_expense)
    trans=Transaction.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request,'dashboard.html',{"transactions":trans,"total_expense":total_expense,'total_income':total_income,'balance':balance})

@login_required
def edit_transaction(request,t_id):
    trans=get_object_or_404(Transaction,pk=t_id,user=request.user)

    if request.method=='POST':
        form=TransactionForm(request.POST);
        if form.is_valid():
            t_name=form.cleaned_data['transaction_name']
            amount=form.cleaned_data['amount']
            t_type=form.cleaned_data['transaction_Type']
            date=form.cleaned_data['date']
            category=form.cleaned_data['category']

            
            transaction=Transaction(t_name=t_name,amount=amount,type=t_type,
            category=category,user=request.user,date=date)
            transaction.save()
            return redirect("dashboard")
    

    else:
        form=TransactionForm(initial={
            "transaction_name":trans.t_name,
            "amount":trans.amount,
            "transaction_type":trans.type,
            "category":trans.category,
            "date":trans.date
        })


    return render(request,'add_transaction.html',{'form':form})

@login_required
def delete_transaction(request,t_id):
    trans=get_object_or_404(Transaction,pk=t_id,user=request.user)
    trans.delete()
    return redirect("transactions")
    
@login_required
def get_analytics(request):

    today=timezone.now()
       

    stats=Transaction.objects.filter(user=request.user, 
        created_at__month=today.month, 
        created_at__year=today.year
    ).aggregate(
        current_total_income=Sum('amount', filter=Q(type='income')),
        current_total_expense=Sum('amount', filter=Q(type='expense')),
    )

    income=stats['current_total_income']
    expense=stats['current_total_expense']


    
    savings_rate=((income-expense)/income * 100) if income !=None and income > 0 else 0
    burn_rate=expense/today.day if income!=None and today.day > 0 else 0
    projected_spending=burn_rate*30

    category_results=(Transaction.objects.filter(user=request.user).values('category__c_name').annotate(total=Sum('amount')))

    

    c_labels=[item['category__c_name'] for item in category_results]

    c_values=[float(item['total']) for item in category_results]


    expense_insights=Transaction.objects.filter(user=request.user,type='expense').values('date__month').annotate(total=Sum('amount'))

    income_insights=Transaction.objects.filter(user=request.user,type='income').values('date__month').annotate(total=Sum('amount'))

    e_labels=[calendar.month_name[item['date__month']]  for item in expense_insights]

    e_values=[float(item['total'])  for item in expense_insights]

    i_values=[float(item['total'])  for item in income_insights]



    # day_insights=Transaction.objects.values(ExtractWeekDay('date')).annotate(total=Sum('amount'))
   
   

    return render(request,'analytics.html',{'c_labels':c_labels,
    'c_values':c_values or [],
    "e_labels":e_labels or [],
    "e_values":e_values or [],
    "i_values":i_values or [],
    'savings_rate': round(savings_rate, 1) or 0,
    'burn_rate': round(burn_rate, 2) or 0,
    'projected_spending': round(projected_spending, 2)

    })

