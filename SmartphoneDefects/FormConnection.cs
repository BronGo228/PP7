using System;
using System.Windows.Forms;

namespace SmartphoneDefects
{
    public partial class FormConnection : Form
    {
        public FormConnection()
        {
            InitializeComponent();
            txtConn.Text = Db.ConnectionString;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            Db.ConnectionString = txtConn.Text;
            MessageBox.Show("Строка подключения обновлена");
            Close();
        }
    }
}
