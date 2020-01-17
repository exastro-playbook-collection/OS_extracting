# OS設定 パラメータ生成ロール

## Trademarks

- Linuxは、Linus Torvalds氏の米国およびその他の国における登録商標または商標です。
- RedHat、RHEL、CentOSは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
- Windows、PowerShellは、Microsoft Corporation の米国およびその他の国における登録商標または商標です。
- Ansibleは、Red Hat, Inc.の米国およびその他の国における登録商標または商標です。
- pythonは、Python Software Foundationの登録商標または商標です。
- NECは、日本電気株式会社の登録商標または商標です。
- その他、本ロールのコード、ファイルに記載されている会社名および製品名は、各社の登録商標または商標です。

## Description

本ロールでは、RHEL7.x や Windows Server 2016 構築済み環境から設定情報を収集する機能と、収集した設定情報からOS設定ロールで使用できるパラメータを生成する機能を提供します。

* 注意事項
  * 本ロールは多数のOS情報を収集するため、環境によっては対象サーバー一台あたりで10~20分以上の時間がかかる場合がありますのでご注意ください。

## Supports

本ロールは、以下環境をサポートします。

- 管理サーバー（Ansible実行サーバー）
  - OS：RHEL7.x（CentOS7.x）
  - Ansible：Version 2.7
  - Python：2.7
- 対象サーバー
  - OS：RHEL7.x（CentOS7.x）
  - OS：Windows Server 2016

## Dependencies

本ロールでは、以下のロール、共通部品を利用しています。

- 収集機能（OS_gathering）
  - gathering ロール
  - OS設定ロール (*1)
- パラメータ生成機能（OS_extracting）
  - パラメータ生成共通部品

(*1) 本ロールを使用する場合、最新のOS設定ロールが必要となります。既存のOS設定ロールを使用しておられる場合、最新版に置き換えてください。

## Role Variables

本ロールで指定できる変数値について説明します。

### Mandatory Variables

ロール利用時に必ず指定しなければならない変数値はありません。

### Optional Variables

ロール利用時に以下の変数値を指定することができます。

- 共通

    | Name                            | Default Value | Description                        |
    | ------------------------------- | ------------- | ---------------------------------- |
    | `VAR_OS_gathering_dest`         |'{{ playbook_dir }}/_gathered_data' | 収集した設定情報の格納先パス |

- OS_gathering
                                                                                                                                                        
    | Name                            | Default Value | Description                        |
    | ------------------------------- | ------------- | ---------------------------------- |
    | `VAR_OS_gathering_rolename`     | (*1)          | 収集対象                            |

- OS_extracting

    | Name                            | Default Value | Description                        |
    | ------------------------------- | ------------- | ---------------------------------- |
    | `VAR_OS_extracting_rolename`    | (*1)          | パラメータ生成対象                     |
    | `VAR_OS_extracting_dest`        | '{{ playbook_dir }}/_parameters' | 生成したパラメータの出力先パス |

    (*1) 本変数値は収集・パラメータ生成時の識別子として使用するため、通常は変更しないでください。

    | No. | OS設定ロール名 | 備考 |
    | --- | ----------- | ---- |
    | 1-01 | `RHEL/NEC_RH_domain` | 対応済 |
    | 1-02 | `RHEL/NEC_RH_grub2` | 対応済 |
    | 1-03 | `RHEL/NEC_RH_kdump` | 対応済 |
    | 1-04 | `RHEL/NEC_RH_keyboard` | 対応済 |
    | 1-05 | `RHEL/NEC_RH_lang` | 対応済 |
    | 1-06 | `RHEL/NEC_RH_logrotate` | 対応済 |
    | 1-07 | `RHEL/NEC_RH_name-resolve` | 対応済 |
    | 1-08 | `RHEL/NEC_RH_network-interface` | 対応済 |
    | 1-09 | `RHEL/NEC_RH_ntp` | 対応済 |
    | 1-10 | `RHEL/NEC_RH_password-rules` | 対応済 |
    | 1-11 | `RHEL/NEC_RH_rsyslog` | 対応済 |
    | 1-12 | `RHEL/NEC_RH_runlevel` | 対応済 |
    | 1-13 | `RHEL/NEC_RH_snmpd` | 対応済 |
    | 1-14 | `RHEL/NEC_RH_sshd` | 対応済 |
    | 1-15 | `RHEL/NEC_RH_static-route` | 対応済 |
    | 2-01 | `Windows/NEC_WIN_owner-organization` | 対応済 |
    | 2-02 | `Windows/NEC_WIN_error-report` | 対応済 |
    | 2-03 | `Windows/NEC_WIN_ipv6-disabled` | 対応済 |
    | 2-04 | `Windows/NEC_WIN_recover-os` | 対応済 |
    | 2-05 | `Windows/NEC_WIN_dns-suffix` | 対応済 |
    | 2-06 | `Windows/NEC_WIN_windows-update` | 対応済 |
    | 2-07 | `Windows/NEC_WIN_powershell-execution-policy` | 対応済 |
    | 2-08 | `Windows/NEC_WIN_name-resolve` | 対応済 |
    | 2-09 | `Windows/NEC_WIN_network-interface` | 対応済 |
    | 2-10 | `Windows/NEC_WIN_static-route` | 対応済 |
    | 2-11 | `Windows/NEC_WIN_AdminApprovalMode` | 対応済 |
    | 2-12 | `Windows/NEC_WIN_teaming` | 対応済 |
    | 2-13 | `Windows/NEC_WIN_remote-desktop` | 対応済 |
    | 2-14 | `Windows/NEC_WIN_hostname` | 対応済 |
    | 2-15 | `Windows/NEC_WIN_virtual-memory` | 対応済 |
    | 2-16 | `Windows/NEC_WIN_ntp` | 対応済 |
    | 2-17 | `Windows/NEC_WIN_uac` | 対応済 |
    | 2-18 | `Windows/NEC_WIN_dotNET35-Install` | 対応済 |
    | 2-19 | `Windows/NEC_WIN_AdminName-change` | 対応済 |
    | 2-20 | `Windows/NEC_WIN_user-rights-assign` | 対応済 |
    | 2-21 | `Windows/NEC_WIN_ProcessorScheduling` | 対応済 |


## Results

本ロールの出力について説明します。

### 収集した設定情報の格納先

収集した設定情報は以下のディレクトリ配下に格納します。

- `<VAR_OS_gathering_dest>/<ホスト名/IP>/OS/<VAR_OS_gathering_rolename>(「RHEL/」や「Windows/」を除く)/`

本ロールを既定値で利用した場合、以下のように設定情報を格納します。

- 構成は以下のとおり(Windows版・Linux版共通)

    ```none
    <Playbook実行ディレクトリ>/
      +-_gathered_data/
          +-<ホスト名/IP>/
              +-OS/                    # OS設定ロール向け専用なフォルダ
                  +-<OS設定ロール名>/     # 収集データ
                      +-command/
                      |   ：
                      +-files/
                      ：
    ```

### 生成したパラメータの出力例

生成したパラメータは以下のディレクトリ・ファイル名で出力します。

- `<VAR_extracting_dest>/<ホスト名/IP>/OS/<VAR_OS_extracting_rolename>.yml(「RHEL/」や「Windows/」を除く)`

本ロールを既定値で利用した場合、以下のようにパラメータを出力します。

- 構成は以下のとおり(Windows版・Linux版共通)

    ```none
    <Playbook実行ディレクトリ>/
      +-_parameters/
          +-<ホスト名/IP>/
              +-OS/                    # OS設定ロール向け専用なフォルダ
                  +-<OS設定ロール名>.yml  # パラメータ
    ```

## Usage

本ロールの利用例について説明します。

### 既定値で設定情報収集およびパラメータ生成を行う場合

以下の例では既定値で設定情報収集およびパラメータ生成を行います。

- `OS_extracting_windows.yml` (Windows版OS設定用Playbook)

    ```yaml
    ---
    - hosts: WindowsGroup
      become: no
      roles:
        - role: OS_gathering
        - role: OS_extracting
    ```

- `OS_extracting_linux.yml` (Linux版OS設定用Playbook)

    ```yaml
    ---
    - hosts: LinuxGroup
      become: yes
      roles:
        - role: OS_gathering
        - role: OS_extracting
    ```

- 以下のように設定情報とパラメータを出力します。

    ```none
    <Playbook実行ディレクトリ>/
      +-_gathered_data/
      |   +-<ホスト名/IPアドレス>/
      |       +-OS/                      # OS設定ロール向け専用なフォルダ
      |           +-<OS設定ロール名>/       # 収集データ
      |               +-files/
      |               ：
      +-_parameters/
          +-<ホスト名/IPアドレス>/
              +-OS/                      # OS設定ロール向け専用なフォルダ
                  +-<OS設定ロール名>.yml    # パラメータ
    ```

### パラメータ再利用

以下の例では、生成したパラメータを使用して構築済Windows/Linuxの設定を変更します。

- `OS_setup.yml`（Linux版OS設定ロールを使用）

    ```yaml
    ---
    - hosts: LinuxGroup
      become: yes
      roles:
        - RHEL/NEC_RH_grub2
    ```

- 生成したパラメータを指定してplaybookを実行

    ```sh
    ansible-playbook OS_setup.yml -i hosts --extra-vars="@_parameters/<ホスト名/IP>/OS/NEC_RH_grub2.yml"
    ```

## Copyright

Copyright (c) NEC Corporation 2019
