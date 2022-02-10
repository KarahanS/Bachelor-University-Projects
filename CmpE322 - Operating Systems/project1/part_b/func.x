/* Arguments for the function are specified. */
struct S {
    int a;
    int b;
    string c<>;
};

program FUNC_PROG{
    version FUNC_VERS{
        string FUNC(S)=1;
    }=1;
}=0x12345678;