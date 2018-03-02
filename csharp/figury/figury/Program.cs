using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace figury
{
    class Kostka
    {
        int a = 0;
        int b = 0;
        int c = 0;

        public Kostka(int a1, int b1, int c1)
        {
             a = a1;
             b = b1;
             c = c1;
        }

        public int Vol()
        {
            return a * b * c;
        }

        public int Area() => 2 * ((a * b) + (a * c) + (b * c));

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
    class Program
    {
        static void Main(string[] args)
        {
            int num;
            int q, w, e;
            string wybor;


            do
            {
                Console.Clear();
                Console.WriteLine("Wybierz intersujaca Cie figure");
                Console.WriteLine("program zapyta o jej wymiary");
                Console.WriteLine("nastepnie wyswietli objetosc oraz pole powierzchni");
                Console.WriteLine("1 Prostopadloscian");
                Console.WriteLine("2 Stozek");
                Console.WriteLine("3 Wyjscie");
                Console.Write("Wprowadz liczbe: ");
                wybor = Console.ReadLine();

                if (!Int32.TryParse(wybor, out num)) continue;

                if (wybor == "3")
                {
                    Environment.Exit(0);
                }

                Console.WriteLine("Wybrano = " + wybor);

                if (wybor == "1")
                {
                    Console.Clear();
                    Console.WriteLine("Wprowadz dlugosci bokow prostopadloscianu: ");
                    q = int.Parse(Console.ReadLine());   //tutaj musze zrobic wychwycenie wprowadzenia czegos
                    w = int.Parse(Console.ReadLine());   //innego niz cyfra -> moze tak jak przy wyborze menu
                    e = int.Parse(Console.ReadLine());
                    Kostka k1 = new Kostka(q, w, e);
                    Console.WriteLine("Objetosc prostopadloscianu jest rowna {0}", k1.Vol());
                    Console.WriteLine("Powierzchnia prostopadloscianu jest rowna {0}", k1.Area());
                    Console.WriteLine("Nacisnij dowolny klawisz by powrocic");
                    Console.ReadKey();
                }
                else if (wybor == "2")
                {
                    Console.Clear();
                    Console.WriteLine("Wprowadz promien i wysokosc stozka: ");
                    q = int.Parse(Console.ReadLine());  //to samo tutaj z wprowadzaniem
                    w = int.Parse(Console.ReadLine());
                    Stozek s1 = new Stozek(q, w);
                    Console.WriteLine("Objetosc stozka jest rowna {0}", s1.Vol());
                    Console.WriteLine("Powierzchnia stozka jest rowna {0}", s1.Area());
                    Console.WriteLine("Nacisnij dowolny klawisz by powrocic");
                    Console.ReadKey();
                }

            } while (true);
        }

    }
}
