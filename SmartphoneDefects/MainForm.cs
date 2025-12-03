using System;
using System.Windows.Forms;

namespace SmartphoneDefects
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void btnDefects_Click(object sender, EventArgs e)
        {
            new FormDefects().ShowDialog();
        }

        private void btnConnection_Click(object sender, EventArgs e)
        {
            new FormConnection().ShowDialog();
        }
        private void btnInspections_Click(object sender, EventArgs e)
        {
            // Ваша логика для кнопки "Инспекции"
            MessageBox.Show("Открытие формы инспекций");
            // Пример: new FormInspections().ShowDialog();
        }

        private void btnImages_Click(object sender, EventArgs e)
        {
            // Ваша логика для кнопки "Изображения"
            MessageBox.Show("Открытие формы изображений");
            // Пример: new FormImages().ShowDialog();
        }
    }
}