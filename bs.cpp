#include<iostream>
class Integer{
    int m,n;
    public:
    Integer(){
        m=0;
        n=1;
    }
    void print(){
        cout<<m<<"and"<<n<<endl;
    }

};
int main(){
    Integer obj;
    obj.print();
    return 0;
}