
int getPos(int i, int j, int n){
	return j+n*i;
}

float distancia(float2 A, float2 B){
	return sqrt(pown(B.x-A.x,2)+pown(B.y-A.y,2));
}

__kernel void is_core(__global const float2 *points, __global const float2 *matriz, __global int *resultados, int k, float epsilon, int ancho ){
	
	int idx = get_global_id(0);

	if(idx==0) printf("%f\n", epsilon);
	if(idx==0) printf("%d\n", k);
	if(idx==0) printf("%d\n", ancho);

	int nrVec = 0;

	float2 A = points[idx];
	if(idx==0) printf("[%d] -- (%f,%f) - Ax, Ay\n", idx, A.x, A.y);

	for(int i=0;i<ancho;i++){
		
		float2 B = matriz[getPos(idx,i,ancho)];
		if(idx==0){
			
			printf("[%d] -- (%f,%f) - Bx, By\n", idx, B.x, B.y);
		}
		
		if(distancia(A,B) <= epsilon) nrVec++;
		if(nrVec>=k) {
			//printf("is core : %d \n", idx);
			resultados[idx] = 1;
			return;
		}

	}
	printf("is not core : %d \n", idx);
	resultados[idx] = 0;
}