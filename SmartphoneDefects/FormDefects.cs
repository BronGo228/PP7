using System;
using System.Windows.Forms;

namespace SmartphoneDefects
{
    public partial class FormDefects
    {
        public FormDefects()
        {
            InitializeComponent();
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Добавлен новый дефект!");
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Дефект изменен!");
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Дефект удален!");
        }
    }
}