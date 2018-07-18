
int getPos(int i, int j, int n){
	return j+n*i;
}

float distancia(float2 A, float2 B){
	return sqrt(pown(B.x-A.x,2)+pown(B.y-A.y,2));
}

__kernel void isCore(__global const float2 *points, __global const int *matriz, __global int *resultados, int k, float epsilon, int ancho ){
	
	int idx = get_global_id(0);
	int nrVec = 0;

	float2 A = points[idx];

	for(int i=0;i<ancho;i++){
		
		int indexB = matriz[getPos(idx,i,ancho)];
		float2 B = points[indexB];

		// if(idx==0){
			
		// 	printf("thread:[%d] i:%d -- index: %d --coords: (%f,%f) - Bx, By\n", idx, i, indexB, B.x, B.y);
		// }
		
		if(distancia(A,B) <= epsilon) nrVec++;
		if(nrVec>=k) {
			//printf("is core : %d \n", idx);
			resultados[idx] = 1;
			return;
		}

	}
	//printf("is not core : %d \n", idx);
	resultados[idx] = 0;
}

__kernel void isBorder(__global const float2 *points, __global const int *matriz, __global int *resultados, float epsilon, int ancho){

	int idx = get_global_id(0);

	if(resultados[idx] == 0){
		float2 A = points[idx];
		for(int i=0; i < ancho; i++){
			int indexB = matriz[getPos(idx,i,ancho)];
			if(resultados[indexB] == 1){
				float2 B = points[indexB];
				if(distancia(A,B) <= epsilon){
					resultados[idx] = 2;
					return;
				}
			}			
		}
	}
}

__kernel void isCoreNxN(__global const float2 *points, __global int *resultados, int k, float epsilon, int ancho ){
	
	int idx = get_global_id(0);
	int nrVec = 0;

	float2 A = points[idx];

	for(int i=0;i<ancho;i++){
		
		float2 B = points[i];
		
		if(distancia(A,B) <= epsilon && idx != i) nrVec++;
		if(nrVec>=k) {
			//printf("is core : %d \n", idx);
			resultados[idx] = 1;
			return;
		}

	}
	//printf("is not core : %d \n", idx);
	resultados[idx] = 0;
}

__kernel void isBorderNxN(__global const float2 *points, __global int *resultados, float epsilon, int ancho){

	int idx = get_global_id(0);

	if(resultados[idx] == 0){
		float2 A = points[idx];
		for(int i=0; i < ancho; i++){
			if(resultados[i] == 1){
				float2 B = points[i];
				if(distancia(A,B) <= epsilon){
					resultados[idx] = 2;
					return;
				}
			}			
		}
	}
}