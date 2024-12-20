﻿using System;
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
    /// 
    /// </summary>
    public partial class MainWindow : Window
    {
        SerialPort serialPort1 = new SerialPort();
        public MainWindow()
        {
            opencom();
            InitializeComponent();
        }
        public void opencom()
        {
            try
            {
                serialPort1.BaudRate = 9600;
                serialPort1.DataBits = 8;
                serialPort1.PortName = "COM2";
                
                serialPort1.StopBits = System.IO.Ports.StopBits.One;
                
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
        }

        private void Click_B(object sender, RoutedEventArgs e)
        {
            candidate.Text = "Teacher Huang\n";
        }

        private void Click_C(object sender, RoutedEventArgs e)
        {
            candidate.Text = "Student Chu\n";
        }

        private void Click_Submit(object sender, RoutedEventArgs e)
        {
            if (candidate.Text != "")
            {
                String total = "Are you sure you want to vote for " + candidate.Text + "?";
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
                MessageBox.Show("Please select a candidate", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }
    }
}
