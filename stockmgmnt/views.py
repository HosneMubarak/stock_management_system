from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.

def home(request):
    title = 'Stock Management System'
    context = {
        'title': title
    }
    return render(request, 'home.html', context)


def list_items(request):
    queryset = Stock.objects.all()
    title = 'List Of Items'
    form = StockSearchForm(request.POST or None)
    if request.method == 'POST':
        queryset = Stock.objects.filter(item_name__icontains=form['item_name'].value())

        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="list of stock.csv"'

            writer = csv.writer(response)
            writer.writerow(['Category', 'Item Name', 'Quantity'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

    context = {
        'title': title,
        'queryset': queryset,
        'form': form,
    }
    return render(request, 'list_items.html', context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    title = 'Add Items'
    if form.is_valid():
        form.save()
        messages.success(request, 'Item added')
        return redirect('/list_items')

    context = {
        'form': form,
        'title': title
    }
    return render(request, 'add_items.html', context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated')
            return redirect('list-items')
    context = {
        'form': form,
        'title': 'Update Item'
    }
    return render(request, 'update_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Item deleted')
        return redirect('list-items')
    context = {
        'title': 'Delete Item',
        'queryset': queryset
    }
    return render(request, 'delete_items.html', context)


def stock_details(request, pk):
    queryset = Stock.objects.get(id=pk)
    return render(request, 'stock_details.html',
                  context={'stock': queryset, 'title': 'Stock Details', 'name': queryset.item_name})


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.save()
        messages.success(request, "issue successfully. " + str(instance.issue_quantity) + " " + str(
            instance.item_name) + " now left in store")
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        'queryset': queryset,
        'title': 'Received' + str(queryset.item_name),
        'form': form,
    }
    return render(request, 'issue_item.html', context)


def receive_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received successfully. " + str(instance.receive_quantity) + " " + str(
            instance.item_name) + " now left in store")
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        'queryset': queryset,
        'title': "Received" + str(queryset.item_name),
        'form': form,
    }
    return render(request, 'receive_items.html', context)


def reorder_level_view(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level successfully Save.")
        return redirect('list-items')
    context = {
        'title': 'Reorder Items',
        'form': form,
        'instance': queryset,
    }
    return render(request, 'reorder_level.html', context)
