# Cealing Host Pymake

本项目提供了 Python 实现的 [Cealing-Host](https://github.com/SpaceTimee/Cealing-Host) Generator，用于生成 Cealing-Host 的配置文件，支持 IP 优选功能。

~~起因是因为不知道为什么 SpaceTimee 的 Generator 不能用，虽然我已经很久没有 Pull 了但是写都写了。~~

## 安装

克隆项目到本地然后安装依赖：

```bash
pip install -r requirements.txt
```

## 配置

`config.jsonc` 文件是配置文件。关于此文件的示例见后。

对于 `WebListFile` 参数指定的文件，该文件将会用作程序的输入，每一行填写一个域名，用以解析，除此之外没有任何其他字符，例如：

```txt
google.com
discord.com
discord.gg
```

当配置完这两项后就可以运行了，参见 ##使用。

## 使用

配置好 `config.jsonc` 后，运行：

```bash
python hostmaker.py
```

等待即可！

## `config.jsonc` 示例

```jsonc
{
    // OutputFile:
    // The result of cealing rules will be written in the specific file.
    // You can use ">" to write to the terminal.
    // You can also use "|" to write nothing.
    // Default: output.json
    "OutputFile": "output.json",

    // ConvertIPv6ToIPv4:
    // Decide if the program will convert IPv6 to IPv4 while adding to the host list.
    // - true (Default)
    // - false
    "ConvertIPv6ToIPv4": false,

    // SelectIP
    // Decide if the program will choose the fastest IP address for the website input.
    // - true (Default)
    // - false
    "SelectIP": true,

    // WebListFile
    // The file path of the website list.
    // Default: weblist.txt
    "WebListFile": "./weblist.txt"
}
```
