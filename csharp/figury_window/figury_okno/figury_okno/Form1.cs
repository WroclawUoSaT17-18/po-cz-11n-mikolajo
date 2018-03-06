using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace figury_okno
{
        public partial class Form1 : Form
    {
        double liczba1, liczba2, liczba3;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            liczba1 = Convert.ToDouble(txtA.Text);
            liczba2 = Convert.ToDouble(txtB.Text);
            liczba3 = Convert.ToDouble(txtC.Text);

            if (radioVol.Checked)
            {
                Kostka k1 = new Kostka(liczba1, liczba2, liczba3);
                txtVol.Text = k1.Vol().ToString();
                txtArea.Text = k1.Area().ToString();
            }

            if (radArea.Checked)
            {
                Stozek s1 = new Stozek(liczba1, liczba2);
                txtVol.Text = s1.Vol().ToString();
                txtArea.Text = s1.Area().ToString();
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void txtA_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar)
             && !char.IsDigit(e.KeyChar)
             && e.KeyChar != '.')
            {
                e.Handled = true;
            }
        }

        private void txtB_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar)
             && !char.IsDigit(e.KeyChar)
             && e.KeyChar != '.')
            {
                e.Handled = true;
            }
        }

        private void txtC_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (!char.IsControl(e.KeyChar)
             && !char.IsDigit(e.KeyChar)
             && e.KeyChar != '.')
            {
                e.Handled = true;
            }
        }

        class Kostka
        {
            double a = 0;
            double b = 0;
            double c = 0;

            public Kostka(double a1, double b1, double c1)
            {
                a = a1;
                b = b1;
                c = c1;
            }

            public double Vol()
            {
                return a * b * c;
            }

            public double Area() => 2 * ((a * b) + (a * c) + (b * c));

            ~Kostka() { }  //nie jestem pewny do uzycia destruktora
        }

        class Stozek
        {
            double r = 0;
            double h = 0;

            public Stozek(double r1, double h1)
            {
                r = r1;
                h = h1;
            }

            public double Vol() => (Math.PI * Math.Pow(r, 2) * h) / 3;

            public double Area() => (Math.PI * r * (r + Math.Sqrt(Math.Pow(h, 2) + Math.Pow(r, 2))));

            ~Stozek() { }  //nie jestem pewny do uzycia destruktora

        }


    }
}
