# HostEditor.py

class HostEditor:
    """
    Host 编辑操作接口。
    """

    def __init__(self, hostsPath: str = "C:/Windows/System32/drivers/etc/hosts",
                 rangeStartSign: str = None, rangeEndSign: str = None,
                 encoding = "utf-8"):
        """
        初始化。

        @param hostsPath: hosts 文件路径。
        @param rangeStartSign: 程序管辖范围的起始标记。
        @param rangeEndSign: 程序管辖范围的结束标记。
        @param encoding: hosts 文件编码。
        """
                
        self.hostsPath = hostsPath
        self.encoding = encoding

        # hosts 文件中，不需要改动的原文
        # [0]: 前半部分，[1]: 后半部分
        # 期待的 Hosts 格式：
        # [0] ..程序编辑的部分.. [1]
        self.rawContents: list[str] = []

        # hosts 文件中，需要改动的部分
        self.hostConfigs: dict[str, str] = {}

        # 用以标记程序管辖范围的起始和结束行
        self.rangeStartSign = \
            rangeStartSign if rangeStartSign is not None else "# Start HostEd"
        self.rangeEndSign = \
            rangeEndSign if rangeEndSign is not None else "# End HostEd"

    def __AnalizeHowsContent(self, lines: list[str]):
        """
        分析 hosts 文件内容。
        """

        # 标记程序读取到的部分
        # 1: 原始的、不需要改动的部分
        # 2: 需要改动的部分
        # 3: 原始的、不需要改动的部分，在 2 部分后
        indexReadPart = 1

        for line in lines:
            if line.startswith(self.rangeStartSign):
                indexReadPart = 2
                continue
            elif line.startswith(self.rangeEndSign):
                indexReadPart = 3
                continue

            if indexReadPart == 1:
                if len(self.rawContents) == 0: self.rawContents.append(line)
                else: self.rawContents[0] += line
                continue
            elif indexReadPart == 3:
                if len(self.rawContents) == 1: self.rawContents.append(line)
                else: self.rawContents[1] += line
                continue
            
            # 分析需要改动的部分
            # 期待的格式：
            # [ip] [domain] #[comment]

            line = line.strip()
            if line == "" or line.startswith("#"): continue

            # 删除注释
            line = line.split("#")[0]

            # 分割 ip 和 domain
            ip, domain = line.split()
            self.hostConfigs[domain] = ip

    def Read(self, doMergeWithOriginalContents: bool = True):
        """
        读取 hosts 文件内容。

        @param doMergeWithOriginalContents: 是否将读取到的内容与原始内容合并。
        """

        self.rawContents = []
        if doMergeWithOriginalContents:
            self.hostConfigs = {}

        with open(self.hostsPath, "r", encoding=self.encoding) as f:
            self.__AnalizeHowsContent(f.readlines())

    def Write(self):
        """
        将 hosts 文件内容写入 hosts 文件。
        """

        with open(self.hostsPath, "w", encoding=self.encoding) as f:
            f.write(self.rawContents[0])
            if self.rawContents[-1][-1] not in ['\n', '\r']:
                f.write("\n")
            f.write("%s\n" % self.rangeStartSign)
            for domain, ip in self.hostConfigs.items():
                f.write("%s %s\n" % (ip, domain))
            f.write(self.rangeEndSign + "\n")
            if len(self.rawContents) >= 2: f.write(self.rawContents[1])

# 测试用
if __name__ == "__main__":
    editor = HostEditor("./test.txt")
    editor.Read()
    editor.Write()