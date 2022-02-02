using Sharprompt;
using System;
using Console = Colorful.Console;
using System.IO;
using System.Drawing;

namespace InitBliveCliper
{
    class ConfigReader
    {
        private string[] fileDetails = new string[1] { "" };
        // 第1行：bc主文件路径
        // 第2行：ffmpeg路径（如果是no就代表没有）
        // 第3行：主播UID
        // 第4行：切片MAN名字
        private const string PATH = @"initedBC.conf"; //配置文件path
        public ConfigReader()
        {
            string[] t_ = File.ReadAllLines(PATH);
            fileDetails = new string[t_.Length];
            fileDetails = t_;
        }
        public string ReadBCWhere() //bc主文件路径
        {
            return fileDetails[0];
        }
        public string ReadUIDWhere()
        {
            return fileDetails[2];
        }
        public string ReadCMan()
        {
            return fileDetails[3];
        }

    }
    class Program
    {
        private static void StepFailed(int step,string firstStepInfo, string secondStepInfo, string finalStepInfo)
        {
            if (step == 1)
            {
                Console.Clear();
                Console.Write("1. " + firstStepInfo, Color.Red);
                Console.Write("  >>  2. " + secondStepInfo + "  >>  3. " + finalStepInfo + "\n");
                Console.WriteLine("");
            }
            else if (step == 2)
            {
                Console.Clear();
                Console.Write("1. " + firstStepInfo, Color.Green);
                Console.Write("  >>  ");
                Console.Write("2. " + secondStepInfo, Color.Red);
                Console.Write("  >>  3. " + finalStepInfo + "\n");
                Console.WriteLine("");
            }
            else if (step == 3)
            {
                Console.Clear();
                Console.Write("1. " + firstStepInfo, Color.Green);
                Console.Write("  >>  ");
                Console.Write("2. " + secondStepInfo, Color.Green);
                Console.Write("  >>  ");
                Console.Write("3. " + finalStepInfo + "\n", Color.Red);
                Console.WriteLine("");
            }
        }
        private static void WriteFirstStep(string firstStepInfo,string secondStepInfo,string finalStepInfo)
        {
            Console.Clear();
            Console.Write("1. " + firstStepInfo, Color.Yellow);
            Console.Write("  >>  2. " + secondStepInfo + "  >>  3. " + finalStepInfo + "\n");
            Console.WriteLine("");
        }
        private static void WriteSecondStep(string firstStepInfo, string secondStepInfo, string finalStepInfo)
        {
            Console.Clear();
            Console.Write("1. " + firstStepInfo, Color.Green);
            Console.Write("  >>  ");
            Console.Write("2. " + secondStepInfo, Color.Yellow);
            Console.Write("  >>  3. " + finalStepInfo + "\n");
            Console.WriteLine("");
        }
        private static void WriteFinalStep(string firstStepInfo, string secondStepInfo, string finalStepInfo)
        {
            Console.Clear();
            Console.Write("1. " + firstStepInfo, Color.Green);
            Console.Write("  >>  ");
            Console.Write("2. " + secondStepInfo, Color.Green);
            Console.Write("  >>  3. " + finalStepInfo + "\n",Color.Yellow);
            Console.WriteLine("");
        }
        static void Main(string[] args)
        {
            CheckIsFirstUse();
            while (true)
            {
                Console.Clear();
                Console.WriteLine("欢迎使用Blive Cliper Init Tool");
                string[] choices = new[] { "懒人版初始化", "初始化Blive Cliper", "自动补全FFMPEG", "重置配置文件", "启动Blive Cliper", "关于" };
                var use_Choice = Prompt.Select("选择操作", choices);
                switch (use_Choice)
                {
                    case "懒人版初始化":
                        {
                            EasyInit();
                            break;
                        }
                    case "初始化Blive Cliper":
                        {
                            InitBC();
                            break;
                        }
                    case "自动补全FFMPEG":
                        {
                            FFMPEG();
                            break;
                        }
                    case "启动Blive Cliper":
                        {
                            StartBC();
                            break;
                        }
                    case "重置配置文件":
                        {
                            CheckIsFirstUse(true);
                            break;
                        }
                    case "关于":
                        {
                            Console.WriteLine("关于 InitBliveCliper");
                            Console.WriteLine("版权所有 (c) 2022 Github: MasterYuan418");
                            Console.WriteLine("BliveCliper: https://github.com/EchoXiaoze/Blive_cliper");
                            Console.WriteLine("");
                            Console.ReadKey();
                            break;
                        }
                }
                Console.WriteLine("按任意键回到主菜单.");
                Console.ReadKey();
            }
        }
        static void CheckIsFirstUse(bool reset = false)
        {
            if (File.Exists("initedBC.conf") is false || reset == true)
            {
                StreamWriter sw = null;
                if (reset is false) sw = new StreamWriter("initedBC.conf");
                else sw = new StreamWriter("initedBC.conf"); //以后有用
                if (!reset)
                {
                    Console.WriteLine("找不到配置文件...按任意键进入首次使用引导.", Color.Yellow);
                    Console.ReadKey();
                }
                string first = "填写配置信息";
                string second = "检查配置信息";
                string final = "完成";
                var bc_main = Prompt.Input<string>("请输入Blive Cliper主程序路径(如: C:\\abc)");
                var ffmpeg_where = Prompt.Input<string>("你有ffmpeg吗？如果有请填写路径，没有请填写no（路径请指向ffmpeg.exe所在的文件夹）");
                var target_uid = Prompt.Input<string>("请填写要切片的主播的UID（不是直播间ID!）");
                var target_person = Prompt.Input<string>("请填写切片机主人（即切片机听谁的指令，输入B站名称）");
                bool failed = false;
                Console.WriteLine("配置信息填写完成，按任意键开始检查...");
                Console.ReadKey();
                WriteSecondStep(first, second, final);
                if (Directory.Exists(bc_main) is false || File.Exists(bc_main + "\\Blive_clip.py") is false)
                {
                    Console.WriteLine($"错误：在{bc_main}下找不到'Blive_clip.py'，请核对后重试。", Color.Red);
                    failed = true;
                }
                Console.WriteLine($"有效：{bc_main} => 主程序路径 检查完成。", Color.Green);
                sw.WriteLine(bc_main);
                if (ffmpeg_where == "no") sw.WriteLine("no");
                else if (File.Exists(ffmpeg_where + "\\ffmpeg.exe") is false)
                {
                    Console.WriteLine("找不到ffmpeg.exe", Color.Yellow);
                    sw.WriteLine("no");
                }
                else sw.WriteLine(ffmpeg_where);
                Console.WriteLine($"有效：{ffmpeg_where} => FFMPEG路径 检查完成。", Color.Green);
                if (target_person == "" || target_uid == "")
                {
                    Console.WriteLine($"错误：UID或切片man不能为空！", Color.Red);
                    failed = true;
                }
                else
                {
                    sw.WriteLine(target_uid);
                    sw.WriteLine(target_person);
                    Console.WriteLine($"有效：UID = {target_uid}, 切片MAN名字：{target_person} => 基本配置 检查完成。", Color.Green);
                }
                if (failed == false)
                {
                    Console.WriteLine("正在写入...");
                    sw.Close();
                }
                else
                {
                    Console.WriteLine("发生了错误，不会写入");
                    return;
                }
                Console.WriteLine("按任意键继续");
                Console.ReadKey();
                WriteFinalStep(first, second, final);
                Console.WriteLine("初始化完成，按任意键继续。");
                Console.ReadKey();
            }
            else return; //有配置文件了，不用检查
        }
        static void EasyInit()
        {
            InitBC();
            FFMPEG();
        }
        static void InitBC()
        {
            ConfigReader cr = new ConfigReader();
            Console.WriteLine("正在读取Python版本...");
            System.Diagnostics.Process.Start(cr.ReadBCWhere() + "\\pythonVerReader.bat");
            System.Threading.Thread.Sleep(1200);
            string pyv = File.ReadAllText("pyver.txt");
            // example:
            // Python 3.9.2
            Console.WriteLine($"读取到的Python版本：{pyv}");
            if (pyv.Split('.')[0] != "Python 3" || pyv.Split('.')[1] != "9")
            {
                Console.WriteLine("警告！Python版本异常！预期版本：'Python 3.9.*'，读取到：" + pyv, Color.Yellow);
                var c = Prompt.Select<string>("真的要继续吗？", new string[] { "是", "否" });
                if (c == "否")
                {
                    Console.WriteLine("操作被取消。");
                    return;
                }
                else
                {
                    __bc();
                    return;
                }
            }
            else __bc();
        }
        private static void __bc()
        {
            Console.WriteLine("正在执行Blive Cliper 初始化...");
            ConfigReader cr = new ConfigReader();
            System.Diagnostics.Process.Start("python",cr.ReadBCWhere() + "\\第一次使用请先运行这个.py");
            Console.WriteLine("正在写入UID与切片MAN...");
            string[] main = File.ReadAllLines(cr.ReadBCWhere() + "\\Blive_clip.py");
            main[18] = "uid = '" + cr.ReadUIDWhere() + "'";
            main[19] = "clipman_list = ['" + cr.ReadCMan() + "']";
            File.WriteAllLines(cr.ReadBCWhere() + "\\Blive_clip.py", main);
            Console.WriteLine("写入完成，初始化完毕。", Color.Green);
            Console.WriteLine("按任意键继续");
            Console.ReadKey();
            return;
        }
        static void FFMPEG()
        {
            Console.WriteLine("暂不支持。");
        }
        static void StartBC()
        {
            ConfigReader cr = new ConfigReader();
            Console.WriteLine($"即将启动：{cr.ReadBCWhere() + "\\Blive_clip.py"}");
            System.Diagnostics.Process.Start("python",cr.ReadBCWhere() + "\\Blive_clip.py");
        }
    }
}
