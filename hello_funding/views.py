from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import datetime

import my_settings
from daily_funding.serializers import CompanyAccountSerializer, CompanyBalanceSerializer, CompanyWithdrawalSerializer, \
    InvestingiSerializer
from users.serializers import EmptySerializer
from drf_yasg import openapi
import requests, pickle
from bs4 import BeautifulSoup
from users.models import *
import AES

User = get_user_model()


class HelloViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {

    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'company_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='계좌 정보를 가져오고 싶은 회사 ID'),

        }))
    @csrf_exempt
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def account(self, request):
        """ USER 계좌 정보 가져오기 [token required]"""
        company_id = Company.objects.get(id=int(request.data['company_id']))
        # 세션 시작하기
        session = requests.session()

        try:
            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'rb') as f:
                session.cookies.update(pickle.load(f))
        except:
            username = request.user.register_set.get(company_id=company_id).username.strip()
            password = request.user.register_set.get(company_id=company_id).user_password.strip()

            decrypted_username = AES.AESCipher(bytes(my_settings.key)).decrypt(username)
            decrypted_password = AES.AESCipher(bytes(my_settings.key)).decrypt(password)

            USER = decrypted_username
            PASS = decrypted_password

            login_info = {
                "mb_id": USER,  # 아이디 지정
                "mb_password": PASS,  # 비밀번호 지정
            }

            url_login = "https://www.hellofunding.co.kr/bbs/login_check.php"
            res = session.post(url_login, data=login_info)
            res.raise_for_status()  # 오류가 발생하면 예외가 발생합니다.

            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'wb') as f:
                pickle.dump(session.cookies, f)

        # 마이페이지에 접근하기
        url_mypage = "https://www.hellofunding.co.kr/deposit/deposit.php"
        res = requests.get(url_mypage, cookies=session.cookies)
        res.raise_for_status()

        if '이미 회원이십니다' not in res.text:
            username = request.user.register_set.get(company_id=company_id).username.strip()
            password = request.user.register_set.get(company_id=company_id).user_password.strip()

            decrypted_username = AES.AESCipher(bytes(my_settings.key)).decrypt(username)
            decrypted_password = AES.AESCipher(bytes(my_settings.key)).decrypt(password)

            USER = decrypted_username
            PASS = decrypted_password
            print("여기")
            login_info = {
                "mb_id": USER,  # 아이디 지정
                "mb_password": PASS  # 비밀번호 지정
            }

            url_login = "https://www.hellofunding.co.kr/bbs/login_check.php"
            res = session.post(url_login, data=login_info)
            res.raise_for_status()  # 오류가 발생하면 예외가 발생합니다.

            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'wb') as f:
                pickle.dump(session.cookies, f)

            # 마이페이지에 접근하기
            url_mypage = "https://www.hellofunding.co.kr/deposit/deposit.php"
            res = requests.get(url_mypage, cookies=session.cookies)
            res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        data = soup.select('div.boxArea td span')

        account_holder = data[1].text.split(" ")[4]
        bank = data[1].text.split(" ")[0]
        account_number = data[1].text.split(" ")[2]
        deposit = soup.select_one("span#realtime_point1").text


        try:
            request.user.account_set.create(bank=bank, account_holder=account_holder, account_number=account_number,
                                            deposit=deposit, company_id=company_id, uid=request.user.id)

        except:
            request.user.account_set.filter(uid=request.user.id, company_id=company_id).update(bank=bank,
                                                                                               account_number=account_number,
                                                                                               deposit=deposit)
        query_set = request.user.account_set.get(company_id=company_id)
        serializer = CompanyAccountSerializer(query_set)
        return JsonResponse(serializer.data, safe=False)
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'company_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='투자 요약 정보를 가져오고 싶은 회사 ID'),

        }))
    @csrf_exempt
    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def balance(self, request):
        """ USER 투자 요약 정보 가져오기 [token required] """
        company_id = Company.objects.get(id=int(request.data['company_id']))

        # 세션 시작하기
        session = requests.session()

        try:
            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'rb') as f:
                session.cookies.update(pickle.load(f))

        except:

            username = request.user.register_set.get(company_id=company_id).username.strip()
            password = request.user.register_set.get(company_id=company_id).user_password.strip()

            decrypted_username = AES.AESCipher(bytes(my_settings.key)).decrypt(username)
            decrypted_password = AES.AESCipher(bytes(my_settings.key)).decrypt(password)

            USER = decrypted_username
            PASS = decrypted_password

            login_info = {

                "mb_id": USER,  # 아이디 지정
                "mb_password": PASS  # 비밀번호 지정
            }

            url_login = "https://www.hellofunding.co.kr/bbs/login_check.php"
            res = session.post(url_login, data=login_info)
            res.raise_for_status()  # 오류가 발생하면 예외가 발생합니다.

            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'wb') as f:
                pickle.dump(session.cookies, f)

        # 마이페이지에 접근하기
        url_mypage = "https://www.hellofunding.co.kr/deposit/deposit.php"
        res = session.get(url_mypage)
        res.raise_for_status()

        if '이미 회원이십니다' not in res.text:
            username = request.user.register_set.get(company_id=company_id).username.strip()
            password = request.user.register_set.get(company_id=company_id).user_password.strip()

            decrypted_username = AES.AESCipher(bytes(my_settings.key)).decrypt(username)
            decrypted_password = AES.AESCipher(bytes(my_settings.key)).decrypt(password)

            USER = decrypted_username
            PASS = decrypted_password

            login_info = {
                "mb_id": USER,  # 아이디 지정
                "mb_password": PASS  # 비밀번호 지정
            }

            url_login = "https://www.hellofunding.co.kr/bbs/login_check.php"
            res = session.post(url_login, data=login_info)
            res.raise_for_status()  # 오류가 발생하면 예외가 발생합니다.

            with open('C:/Users/daily-funding/Desktop/cookie/' + str(request.user.id) + '_' + str(
                    company_id.id) + '_cookie.txt', 'wb') as f:
                pickle.dump(session.cookies, f)

            # 마이페이지에 접근하기
            url_mypage = "https://www.hellofunding.co.kr/deposit/deposit.php"
            res = requests.get(url_mypage, cookies=session.cookies)
            res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        total_investment = soup.select("div#invest_status td")[1].text.strip().replace('원', '').replace(',', '')
        residual_investment_price = soup.select("div#invest_status td")[4].text.strip().replace('원', '').replace(',', '')

        num_product_url = "https://www.hellofunding.co.kr/deposit/ajax_repay_stats.php"
        res = session.get(num_product_url, cookies=session.cookies)
        soup = BeautifulSoup(res.text, "html.parser")
        number_of_investing_products = soup.select("td")[1].text.replace("건","").strip()

        try:
            request.user.investing_balance_set.create(total_investment=total_investment,
                                                      number_of_investing_products=number_of_investing_products,
                                                      residual_investment_price=residual_investment_price,
                                                      company_id=company_id, uid=request.user.id)
        except:
            request.user.investing_balance_set.filter(uid=request.user.id, company_id=company_id).update(
                total_investment=total_investment,
                number_of_investing_products=number_of_investing_products,
                residual_investment_price=residual_investment_price)

        query_set = request.user.investing_balance_set.get(company_id=company_id)
        serializer = CompanyBalanceSerializer(query_set)
        return JsonResponse(serializer.data, safe=False)

        return Response(status=status.HTTP_201_CREATED)