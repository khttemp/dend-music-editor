# dend-music-editor

* ja（ 日本語 ）

## 概要

dend-music-editor は、電車でD のBGMリストをGUI画面上で編集するソフトウェアである。

## 動作環境

* 電車でDが動くコンピュータであること
* OS: Windows 10 64bit の最新のアップデートであること
* OSの端末が日本語に対応していること
* 横1024×縦768ピクセル以上の画面解像度があるコンピュータ

※ MacOS 、 Linux などの Unix 系 OS での動作は保証できない。


## 免責事項

このプログラムを使用して発生したいかなる損害も製作者は責任を負わない。

このプログラムを実行する前に、自身のコンピュータのフルバックアップを取得して、
安全を担保したうえで実行すること。
このプログラムについて、電車でD 作者である、地主一派へ問い合わせてはいけない。

このソフトウェアの更新やバグ取りは、作者の義務ではなく解消努力目標とする。
Issue に上げられたバグ情報が必ず修正されるものではない。

* ライセンス：MIT

電車でD の正式なライセンスを持っていること。

本プログラムに関連して訴訟の必要が生じた場合、東京地方裁判所を第一審の専属的合意管轄裁判所とする。

このプログラムのバイナリを実行した時点で、この規約に同意したものと見なす。

## 実行方法

![title](https://github.com/khttemp/dend-music-editor/blob/main/image/title.png)

### BGMリスト編集方法

1. メニュの「ファイルの開く」でバイナリファイルを開く。

    Lightning Stageは、「RAIL*.BIN」を開く

    Burning Stageは、「LS_INFO.BIN」を開く

    Climax Stageは、「SOUNDTRACK_INFO.BIN」を開く

    Rising Stageは、「SOUNDTRACK_INFO_4TH.BIN」を開く。

    必ず、プログラムが書込みできる場所で行ってください

2. 編集したい行を選ぶ

3. 「このBGMを修正する」ボタンで、BGMファイル名や、時間を修正する

4. 「このBGMを入れ替える」ボタンで、リストにある別の行と入れ替える

### プレイヤー設定方法

1. メニュの「BGMファイルを開く」ボタンで、再生したいBGMファイルを開く。

    再生できるBGMは、「ogg、wav」のみである。

2. start、loop start、loop endの入力欄に数字を設定する

    loop endが0より小さい場合（－1など）、曲の最後まで再生する

3. 「Play」ボタンで、ループ設定した通りに再生する。

4. 「Pause」ボタンで、止める。

## ソースコード版の実行方法

このソフトウェアは Python3 系で開発されているため、 Python3 系がインストールされた開発機であれば、
ソースコードからソフトウェアの実行が可能である。


### 依存ライブラリ

* Tkinter

  Windows 版 Python3 系であれば、インストール時のオプション画面で tcl/tk and IDLE のチェックがあったと思う。
  tcl/tk and IDLE にチェックが入っていればインストールされる。
  
  Linux 系 OS では、 パッケージ管理システムを使用してインストールする。

* pygame

  プレイヤーを再生するためのライブラリ。pipでインストールする必要がある。
  
  コマンド例：
  
  ````
  > pip install pygame
  ````
  

### 動作環境

以下の環境で、ソースコード版の動作確認を行った。

* OS: Windows 10 64bit
* Python 3.10.9 64bit
* pygame 2.1.2 64bit
* pip 22.3.1 64bit
* Nuitka 1.3.7 64bit
* 横1024×縦768ピクセル以上の画面解像度があるコンピュータ

  * フルハイビジョン（ 横1920×縦1080ピクセル ）以上の画面解像度があるコンピュータが望ましい

### ソースコードの直接実行

Windows 環境で上記の通り、依存ライブラリがインストール済なら、以下のコマンドを入力する。


````
> python musicEditor.py
````

これで、実行方法に記載した画面が現れれば動作している。

### FAQ

* Q. 電車でD ゲームがあるのに、 指定のバイナリファイル が無い。 
  
  * A. Rising Stageまでの旧作は、Packファイルを

    GARbro のような、アーカイバで展開すると得られる。

  * A. GARbro を使用して空パスワードで解凍すると無効なファイルになるので、適切なパスワードを入力すること。


* Q. BINファイルを指定しても、「予想外のエラーが出ました。電車でDのファイルではない、またはファイルが壊れた可能性があります。」と言われる

  * A. 抽出方法が間違っているか、抽出時のパスワードが間違っているのでは？作業工程をやり直した方がよい。

* Q. BINファイルを改造しても、変化がないけど？

  * A. Rising Stageまでの旧作は、既存のPackファイルとフォルダーが同時にあるなら、

    Packファイルを優先して読み込んでいる可能性がある。

    読み込みしないように、抽出したPackファイルを変更するか消そう。

* Q. ダウンロードがブロックされる、実行がブロックされる、セキュリティソフトに削除される

  * A. ソフトウェア署名などを行っていないので、ブラウザによってはダウンロードがブロックされる

  * A. 同様の理由でセキュリティソフトが実行を拒否することもある。


* Q. MP3 や AAC などその他のファイルも使えるようにしてほしい

  * A. 製作者側で対応すると、特許やライセンス料の問題があるので無理。
  
    本ソフトの利用者が任意の変換ソフトを使用して、  wave か OGG 形式に変換すること。


### Windows 版実行バイナリ（ .exeファイル ）の作成方法

pyinstaller か Nuitka ライブラリをインストールする。 pip でも  easy_install  でも構わない。

下は、 Nuitka を使用して、Windows 版実行バイナリ（ .exeファイル ）を作る例である。

````
> set DDLPATH=%LOCALAPPDATA%\Programs\Python\Python310\Lib\site-packages\pygame
> nuitka --include-data-file=%DDLPATH%\libogg-0.dll=libogg-0.dll --include-data-file=%DDLPATH%\libvorbis-0.dll=libvorbis-0.dll --include-data-file=%DDLPATH%\libvorbisfile-3.dll=libvorbisfile-3.dll --mingw64 --onefile --enable-plugin=tk-inter --follow-imports --remove-output --disable-console musicEditor.py
````

musicEditor.exe が出力される。

### Virustotal

![virustotal](https://github.com/khttemp/dend-music-editor/blob/main/image/virustotal.png)

以上。