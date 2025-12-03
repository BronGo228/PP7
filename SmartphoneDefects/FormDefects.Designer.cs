using System.Windows.Forms;

namespace SmartphoneDefects
{
    partial class FormDefects : Form
    {
        private System.Windows.Forms.DataGridView grid;
        private System.Windows.Forms.TextBox txtType;
        private System.Windows.Forms.TextBox txtDesc;
        private System.Windows.Forms.TextBox txtConf;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnEdit;
        private System.Windows.Forms.Button btnDelete;

        private void InitializeComponent()
        {
            this.grid = new System.Windows.Forms.DataGridView();
            this.txtType = new System.Windows.Forms.TextBox();
            this.txtDesc = new System.Windows.Forms.TextBox();
            this.txtConf = new System.Windows.Forms.TextBox();
            this.btnAdd = new System.Windows.Forms.Button();
            this.btnEdit = new System.Windows.Forms.Button();
            this.btnDelete = new System.Windows.Forms.Button();

            // Настройка DataGridView
            this.grid.Top = 10;
            this.grid.Left = 10;
            this.grid.Width = 500;
            this.grid.Height = 220;

            // Настройка TextBox
            this.txtType.Top = 250;
            this.txtType.Left = 10;
            this.txtType.Width = 140;
            this.txtType.Text = "Тип";

            this.txtDesc.Top = 250;
            this.txtDesc.Left = 160;
            this.txtDesc.Width = 140;
            this.txtDesc.Text = "Описание";

            this.txtConf.Top = 250;
            this.txtConf.Left = 310;
            this.txtConf.Width = 140;
            this.txtConf.Text = "Уверенность";

            // Настройка кнопок
            this.btnAdd.Text = "Добавить";
            this.btnAdd.Top = 300;
            this.btnAdd.Left = 10;
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);

            this.btnEdit.Text = "Изменить";
            this.btnEdit.Top = 300;
            this.btnEdit.Left = 110;
            this.btnEdit.Click += new System.EventHandler(this.btnEdit_Click);

            this.btnDelete.Text = "Удалить";
            this.btnDelete.Top = 300;
            this.btnDelete.Left = 210;
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);

            // Добавление элементов на форму
            this.Controls.Add(this.grid);
            this.Controls.Add(this.txtType);
            this.Controls.Add(this.txtDesc);
            this.Controls.Add(this.txtConf);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.btnEdit);
            this.Controls.Add(this.btnDelete);

            // Свойства формы
            this.Text = "Дефекты";
            this.Width = 550;
            this.Height = 400;
        }
    }
}