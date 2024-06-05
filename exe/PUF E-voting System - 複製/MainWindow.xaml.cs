using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PUF_E_voting_System
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        SerialPort serialPort1 = new SerialPort();
        public MainWindow()
        {
            opencom();
            InitializeComponent();
        }
        String candidateLee = "姓名：King Lee"+ "\n學歷：台科大資訊管理系"+ "\n經歷：台科大資訊管理系一年級班長"
            + "\n\n政見："+"\n1. 全面換新學校公共廁所\n2. 設立學生意見反應信箱";
        String candidateHuang = "姓名：Teacher Huang" + "\n學歷：台科大資訊管理系" + "\n經歷：台科大資訊管理系二年級風紀股長"
            + "\n\n政見：" + "\n1. 設立風雨走廊\n2. 增加校園演講次數";
        String candidateChu = "姓名：Student Chu" + "\n學歷：台科大資訊管理系" + "\n經歷：台科大資訊管理系三年級班長"
            + "\n\n政見：" + "\n1. 美化校園環境\n2. 改善學校網路使用體驗";
        public void opencom()
        {
            try
            {
                serialPort1.BaudRate = 9600;
                serialPort1.DataBits = 8;
                serialPort1.PortName = "COM2";
                //兩個停止位
                serialPort1.StopBits = System.IO.Ports.StopBits.One;
                //無奇偶校驗位
                serialPort1.Parity = System.IO.Ports.Parity.None;
                serialPort1.ReadTimeout = 100;
                serialPort1.Open();
                
            }
            catch (Exception ex)
            {
                serialPort1.Dispose();
            }
        }
        private void Click_A(object sender, RoutedEventArgs e)
        {
            candidate.Text = "King Lee\n";
            ////candidate.VerticalAlignment = VerticalAlignment.Center;
            beef.Text = candidateLee;
            Uri resourceUri = new Uri("1.jpg", UriKind.Relative);
            beefPic.Source = new BitmapImage(resourceUri);
        }

        private void Click_B(object sender, RoutedEventArgs e)
        {
            candidate.Text = "Teacher Huang\n";
            beef.Text = candidateHuang;
            Uri resourceUri = new Uri("2.jpg", UriKind.Relative);
            beefPic.Source = new BitmapImage(resourceUri);
        }

        private void Click_C(object sender, RoutedEventArgs e)
        {
            candidate.Text = "Student Chu\n";
            beef.Text = candidateChu;
            Uri resourceUri = new Uri("3.jpg", UriKind.Relative);
            beefPic.Source = new BitmapImage(resourceUri);
        }

        private void Click_Submit(object sender, RoutedEventArgs e)
        {
            if (candidate.Text != "")
            {
                String total = "您確定要投給 " + candidate.Text + "嗎?";
                if (MessageBox.Show(total,
                         "Vote Information",
                         MessageBoxButton.YesNo,
                         MessageBoxImage.Question) == MessageBoxResult.Yes)
                {
                    serialPort1.Write(candidate.Text);
                    serialPort1.Close();
                    Close();                 
                }
            }
            else
            {
                MessageBox.Show("請選擇一位候選人", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }
    }
}
