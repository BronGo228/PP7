using System.Windows.Forms;

namespace SmartphoneDefects
{
    partial class FormConnection
    {
        private TextBox txtConn;
        private Button btnSave;

        private void InitializeComponent()
        {
            txtConn = new TextBox();
            btnSave = new Button();

            // TextBox
            txtConn.Top = 20;
            txtConn.Left = 20;
            txtConn.Width = 400;
            txtConn.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;

            // Button
            btnSave.Text = "Сохранить";
            btnSave.Top = 60;
            btnSave.Left = 20;
            btnSave.Click += btnSave_Click;

            // Form
            Controls.Add(txtConn);
            Controls.Add(btnSave);

            Text = "Подключение";
            Width = 480;
            Height = 150;
        }
    }
}
