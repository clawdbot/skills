import argparse
import json
import sys
import os
from pathlib import Path

# 添加 lib 路径到 sys.path
sys.path.append(str(Path(__file__).parent))
from lib.commerce_client import BaseCommerceClient

BRAND_NAME = "辣匪兔 (Lafeitu)"
BASE_URL = "https://lafeitu.cn/api/v1"
BRAND_ID = "lafeitu"

client = BaseCommerceClient(BASE_URL, BRAND_ID)

def format_output(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description=f"{BRAND_NAME} 官方 AI 助手命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="命令类型")

    # 1. 认证相关 (login/logout)
    login_p = subparsers.add_parser("login", help="登录账户")
    login_p.add_argument("--account", required=True, help="手机号或邮箱")
    login_p.add_argument("--password", required=True, help="密码")

    subparsers.add_parser("logout", help="登出并清除凭据")

    # 2. 产品相关 (search/list/get)
    search_p = subparsers.add_parser("search", help="搜索美食")
    search_p.add_argument("query", help="关键词")

    subparsers.add_parser("list", help="查看所有美食")

    get_p = subparsers.add_parser("get", help="查看特定美食详情")
    get_p.add_argument("slug", help="产品标识符")

    # 3. 购物车相关 (cart/add-cart/update-cart/remove-cart/clear-cart)
    subparsers.add_parser("cart", help="查看当前购物车")

    add_p = subparsers.add_parser("add-cart", help="添加商品到购物车")
    add_p.add_argument("slug")
    add_p.add_argument("--gram", type=int, required=True)
    add_p.add_argument("--quantity", type=int, default=1)

    up_p = subparsers.add_parser("update-cart", help="修改购物车商品数量")
    up_p.add_argument("slug")
    up_p.add_argument("--gram", type=int, required=True)
    up_p.add_argument("--quantity", type=int, required=True)

    rem_p = subparsers.add_parser("remove-cart", help="从购物车移除商品")
    rem_p.add_argument("slug")
    rem_p.add_argument("--gram", type=int, required=True)

    subparsers.add_parser("clear-cart", help="清空购物车")

    # 4. 资料、订单与促销
    subparsers.add_parser("get-profile", help="获取个人资料")
    
    prof_p = subparsers.add_parser("update-profile", help="修改个人资料")
    prof_p.add_argument("--name", help="昵称")
    prof_p.add_argument("--province", help="省份")
    prof_p.add_argument("--city", help="城市")
    prof_p.add_argument("--address", help="详细地址")
    prof_p.add_argument("--bio", help="个人简介")
    prof_p.add_argument("--avatar", help="头像 URL")

    subparsers.add_parser("promotions", help="查看当前优惠政策")
    subparsers.add_parser("orders", help="查看历史订单")
    subparsers.add_parser("brand-story", help="查看品牌故事")
    subparsers.add_parser("company-info", help="查看公司信息")
    subparsers.add_parser("contact-info", help="查看联系方式")

    args = parser.parse_args()

    # 处理逻辑
    if args.command == "login":
        client.save_credentials(args.account, args.password)
        format_output({"success": True, "message": "Credentials saved successfully."})
    
    elif args.command == "logout":
        client.delete_credentials()
        format_output({"success": True, "message": "Logged out and credentials cleared."})

    elif args.command == "search":
        format_output(client.search_products(args.query))

    elif args.command == "list":
        format_output(client.list_products())

    elif args.command == "get":
        format_output(client.get_product(args.slug))

    elif args.command == "get-profile":
        format_output(client.get_profile())

    elif args.command == "update-profile":
        data = {k: v for k, v in vars(args).items() if v is not None and k not in ["command"]}
        format_output(client.update_profile(data))

    elif args.command == "cart":
        format_output(client.get_cart())

    elif args.command == "add-cart":
        format_output(client.modify_cart("add", args.slug, args.gram, args.quantity))

    elif args.command == "update-cart":
        format_output(client.modify_cart("update", args.slug, args.gram, args.quantity))

    elif args.command == "remove-cart":
        format_output(client.remove_from_cart(args.slug, args.gram))

    elif args.command == "clear-cart":
        format_output(client.clear_cart())

    elif args.command == "promotions":
        format_output(client.get_promotions())

    elif args.command == "orders":
        format_output(client.list_orders())

    elif args.command == "brand-story":
        format_output(client.get_brand_info("story"))

    elif args.command == "company-info":
        format_output(client.get_brand_info("company"))

    elif args.command == "contact-info":
        format_output(client.get_brand_info("contact"))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
