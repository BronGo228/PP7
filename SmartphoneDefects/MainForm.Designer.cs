using System.Windows.Forms;
namespace SmartphoneDefects
{
    partial class MainForm
    {
        private Button btnDefects;
        private Button btnInspections;
        private Button btnImages;
        private Button btnConnection;

        private void InitializeComponent()
        {
            btnDefects = new Button();
            btnInspections = new Button();
            btnImages = new Button();
            btnConnection = new Button();

            btnDefects.Text = "Дефекты";
            btnDefects.Top = 20;
            btnDefects.Left = 20;
            btnDefects.Width = 200;
            btnDefects.Click += btnDefects_Click;

            btnInspections.Text = "Инспекции";
            btnInspections.Top = 60;
            btnInspections.Left = 20;
            btnInspections.Width = 200;
            btnInspections.Click += btnInspections_Click;

            btnImages.Text = "Изображения";
            btnImages.Top = 100;
            btnImages.Left = 20;
            btnImages.Width = 200;
            btnImages.Click += btnImages_Click;

            btnConnection.Text = "Подключение к БД";
            btnConnection.Top = 140;
            btnConnection.Left = 20;
            btnConnection.Width = 200;
            btnConnection.Click += btnConnection_Click;

            Controls.Add(btnDefects);
            Controls.Add(btnInspections);
            Controls.Add(btnImages);
            Controls.Add(btnConnection);

            Text = "Главное меню";
            Width = 260;
            Height = 230;
        }
    }
}
