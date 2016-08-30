#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <set>

using namespace std;

#define LINE (122)
#define NUMBERS (9)
#define NUM_POINT 47

/*
Division_trails stores all the division trails of a given Sbox.
Here, Division_trails contains division trails of PRESENT Sbox,  
*/
int Division_trails[NUM_POINT][8]={ 
{0,0,0,0,0,0,0,0}, 
{0,0,0,1,0,0,0,1}, 
{0,0,0,1,0,0,1,0}, 
{0,0,0,1,0,1,0,0}, 
{0,0,0,1,1,0,0,0}, 
{0,0,1,0,0,0,0,1}, 
{0,0,1,0,0,0,1,0}, 
{0,0,1,0,0,1,0,0}, 
{0,0,1,0,1,0,0,0}, 
{0,0,1,1,0,0,1,0}, 
{0,0,1,1,0,1,0,0}, 
{0,0,1,1,1,0,0,0}, 
{0,1,0,0,0,0,0,1}, 
{0,1,0,0,0,0,1,0}, 
{0,1,0,0,0,1,0,0}, 
{0,1,0,0,1,0,0,0}, 
{0,1,0,1,0,0,1,0}, 
{0,1,0,1,0,1,0,0}, 
{0,1,0,1,1,0,0,0}, 
{0,1,1,0,0,0,0,1}, 
{0,1,1,0,0,0,1,0}, 
{0,1,1,0,1,0,0,0}, 
{0,1,1,1,0,0,1,0}, 
{0,1,1,1,1,0,0,0}, 
{1,0,0,0,0,0,0,1}, 
{1,0,0,0,0,0,1,0}, 
{1,0,0,0,0,1,0,0}, 
{1,0,0,0,1,0,0,0}, 
{1,0,0,1,0,0,1,0}, 
{1,0,0,1,0,1,0,0}, 
{1,0,0,1,1,0,0,0}, 
{1,0,1,0,0,0,1,0}, 
{1,0,1,0,0,1,0,0}, 
{1,0,1,0,1,0,0,0}, 
{1,0,1,1,0,0,1,0}, 
{1,0,1,1,0,1,0,0}, 
{1,0,1,1,1,0,0,0}, 
{1,1,0,0,0,0,1,0}, 
{1,1,0,0,0,1,0,0}, 
{1,1,0,0,1,0,0,0}, 
{1,1,0,1,0,0,1,0}, 
{1,1,0,1,0,1,0,0}, 
{1,1,0,1,1,0,0,0}, 
{1,1,1,0,0,1,0,1}, 
{1,1,1,0,1,0,1,1}, 
{1,1,1,0,1,1,1,0}, 
{1,1,1,1,1,1,1,1}};




typedef struct vector_s{
    int a[NUMBERS];
    int comp;
    bool operator <(const struct vector_s &b)const
    {
	    return comp < b.comp;
    }
}vector;

typedef struct point_s{
	int a[NUMBERS -1];
	int comp;
	bool operator <(const struct point_s &b)const
    {
	    return comp < b.comp;
    }
}point;


/*
Read linear inequalities from 'Inequalities.txt', and insert each 
inequality into a set container vec.
*/
void Read_inequalities(set<vector> &vec);


/*
Insert all INVALID division trails into a set container poi.
Invalid division trails consists of the complementary set of all 
division trails.  
*/
void Init_point(set<point> &poi);


/*
Choose the FIRST inequality which excludes the most number of 
invalid division trails
*/
vector* Choose_vec(set<vector> &vec,  set<point> &poi);


/*
Delete the division trails in poi which do no satify ineqlaity temp.
*/
void Delete_point(set<point> &poi, vector* temp);

int main() 
{

	//Initialize pro[16][16] and set poi.
	set<point> poi;
	Init_point(poi);

	
	set<vector> vec;
	Read_inequalities(vec);

	cout<<"vec size = "<<vec.size()<<endl;
	cout<<"point size = "<<poi.size()<<endl;

	set<vector> vec_res;
	set<vector>::iterator it_v;

	while(!poi.empty())
	{
		vector* temp;
		temp = Choose_vec(vec, poi);
		
		vec_res.insert((*temp));
		vec.erase((*temp));

		Delete_point(poi, temp);

		free(temp);
	}
	cout<<"vec_res size = "<<vec_res.size()<<endl;

	//output the vectors remained into Reduced_vector.txt file
	ofstream fout;
	fout.open("Reduced_Inequalities.txt");
	fout<<"[";
	for(it_v = vec_res.begin(); it_v != vec_res.end(); it_v++)
	{
		fout<<"[";
		for(int i = 0; i < NUMBERS-1; i++)
			fout<<(*it_v).a[i]<<", ";
		fout<<(*it_v).a[NUMBERS-1];
		fout<<"],\\"<<endl;
	}
	fout<<"]";
	fout.close();
	return 0;
}
 


void Read_inequalities(set<vector> &vec) 
{
	string str;

	ifstream fin("Inequalities.txt");

	int line, count, index;

	for ( line = 0; line < LINE; line++) 
	{
		getline(fin, str);
		stringstream sstr;
		sstr<<str;
		vector temp; 
		for(int i = 0; i < NUMBERS; i++)
		{
			sstr >> temp.a[i];
		}
		temp.comp = line;
		vec.insert(temp);
	}
	fin.close();
}


void Init_point(set<point> &poi)
{

	point temp;

	for(int i = 0; i < 256; i++)
	{
		for(int j = 0; j < 8; j++)
			temp.a[j] = ((i >> (7-j)) & 0x1);
		temp.comp = i;
		poi.insert(temp);
	}

	for(int i = 0; i < NUM_POINT; i++)
	{
		int compare = 0;
		for(int j = 0; j < NUMBERS-1; j++)
		{
			compare = (compare << 1);
			temp.a[j] = Division_trails[i][j];
			compare = (compare ^ temp.a[j]); 
		}
		temp.comp = compare;
		poi.erase(temp); 
	}
	
}



vector* Choose_vec(set<vector> &vec,  set<point> &poi)
{
	set<vector>::iterator it_v;
	set<point>::iterator it_p;

	vector* temp = (vector*)malloc(sizeof(vector));

	int record = -1;
	for( it_v = vec.begin(); it_v != vec.end(); it_v++)
	{
		int counter = 0;
		for( it_p = poi.begin(); it_p != poi.end(); it_p++)
		{
			int t1 = 0;
			for(int i = 0; i < (NUMBERS - 1); i++)
				t1 = t1 + ((*it_v).a[i] * (*it_p).a[i]);
			t1 = t1 + (*it_v).a[NUMBERS -1];
			if(t1 < 0)
				counter++;
		}
		if(counter > record)
		{
			record = counter;
			for(int s = 0; s < NUMBERS; s++)
				(*temp).a[s] = (*it_v).a[s];
			(*temp).comp = (*it_v).comp;
		}
	}
	return temp;
}


void Delete_point(set<point> &poi, vector* temp)
{
	set<point>::iterator it_p;
	for( it_p = poi.begin(); it_p != poi.end(); it_p++)
	{
		int t1 = 0;
		for(int i = 0; i < (NUMBERS - 1); i++)
			t1 = t1 + ((*it_p).a[i] * (*temp).a[i]);
		t1 = t1 + (*temp).a[NUMBERS -1];
		if(t1 < 0)
			poi.erase(it_p);
	}
}