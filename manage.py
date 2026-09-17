#!/usr/bin/env python3
"""Djangoの管理コマンドを実行する入口。"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Djangoが見つかりません。README.mdの手順で仮想環境を作り、"
            "依存パッケージをインストールしてください。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
