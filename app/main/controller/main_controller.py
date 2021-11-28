import os

from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory
import pandas as pd

user_route = Blueprint('user_route', __name__)

@user_route.route('/', methods=['GET'])
def main():
  return render_template('index.html', title="메인")

@user_route.app_errorhandler(404)
def not_find(err):
  return render_template('common/404.html', title="404"), 404

@user_route.app_errorhandler(500)
def internal_error(err):
  return render_template('common/500.html', title="500"), 500

@user_route.route('/club', methods=['GET'])
def club():
  club_info = pd.read_csv('./app/main/static/files/club_info.csv')
  club_info = club_info[['CTPRVN_NM', 'SIGNGU_NM', 'ITEM_NM', 'TROBL_TY_NM', 'CLUB_NM', ]]
  club_info = club_info.fillna("-")

  return render_template('club.html', title="동호회", club_info=club_info)

@user_route.route('/filter', methods=['GET','POST'])
def filter():
  select1 = request.form.get('areas')
  select2 = request.form.get('sports')
  name=request.form.get('name')
  club_info = pd.read_csv('./app/main/static/files/club_info.csv')
  club_info = club_info[['CTPRVN_NM', 'SIGNGU_NM', 'ITEM_NM', 'TROBL_TY_NM', 'CLUB_NM', ]]
  club_info = club_info.fillna("-")
  conta1 = club_info['CTPRVN_NM'].str.contains(select1)
  conta2 = club_info['ITEM_NM'].str.contains(select2)
  club_name = club_info['CLUB_NM'].str.contains(name)


  if select1 =='전체' :
    conta1 = True
  if select2 == '전체' :
    conta2 = True
  if name =='':
    club_name = True
  condi = conta1 &conta2&club_name
  club_info2 = club_info[condi]
  return render_template('club.html', title="동호회", club_info=club_info2)


