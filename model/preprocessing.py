import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.special import erf

def add_sym(pan,f_sz,n_f):
	# return matrix symetrique enleve les commentaires pr compendre
	#pan=np.array([[1,2,3,4],[5,6,7,8],[-1,-2,-3,-4],[-5,-6,-7,-8]])
	#f_sz = 4
	#n_f  = 1
	(ln_x,ln_y)=pan.shape
	ln_a = f_sz*n_f
	ln_xx = ln_x+ln_a*2
	ln_yy = ln_y+ln_a*2
	pan_add = np.zeros((ln_xx,ln_yy))
	pan_add[ln_a:ln_a+ln_x,ln_a:(ln_a+ln_y)]=pan
	
	for i in range(0,n_f):
		pan_add[(ln_a-f_sz - i*f_sz):(ln_a-i*f_sz),(ln_a):(ln_a+ln_y)] = pan[(0+i*f_sz):(f_sz+i*f_sz),:]
		pan_add[(0+ln_a+ln_x+i*f_sz):(f_sz+ln_a+ln_x+i*f_sz),(ln_a):(ln_a+ln_y)] = pan[(0-f_sz+ln_x-i*f_sz):(f_sz-f_sz+ln_x-i*f_sz),:]
	for i in range(0,n_f):
		
		pan_add[:,(ln_a-f_sz-i*f_sz):(ln_a-i*f_sz)] = pan_add[:,(0+i*f_sz+ln_a):(f_sz+i*f_sz+ln_a)]
		pan_add[:,(0+ln_a+ln_y+i*f_sz):(f_sz+ln_a+ln_y+i*f_sz)] = pan_add[:,(0-f_sz+ln_y-i*f_sz+ln_a):(f_sz-f_sz+ln_y-i*f_sz+ln_a)]
		
	return pan_add

def upsample_perfect(pan2m_mft):
	#pan2m_mft = [[101,103,105],[111,113,115],[121,123,125]]
	#pan2m_mft=np.asarray([[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13]])
	pan2m_mft=np.array(pan2m_mft)
	(l_r,l_c)=pan2m_mft.shape
	row = 4*l_r
	col = 4*l_c
	ln_t = 67
	pos_0 = 33
	signal6 = np.zeros((1,ln_t))
	signal6[0,pos_0] = 1
	signal6[0,pos_0+1] = 2*0.305334091
	signal6[0,pos_0-1] = 2*0.305334091
	signal6[0,pos_0+3] = 2*-0.072698593
	signal6[0,pos_0-3] = 2*-0.072698593
	signal6[0,pos_0+5] = 2*0.021809577
	signal6[0,pos_0-5] = 2*0.021809577
	signal6[0,pos_0+7] = 2*-0.005192756
	signal6[0,pos_0-7] = 2*-0.005192756
	signal6[0,pos_0+9] = 2*0.000807762
	signal6[0,pos_0-9] = 2*0.000807762
	signal6[0,pos_0+11] = 2*-0.000060081
	signal6[0,pos_0-11] = 2*-0.000060081
	signal12 = np.zeros((1,ln_t))
	for i in range(-33,34):
		posi = pos_0+i
		val=0
		for j in range(-11,12):
			posj=pos_0+j;
			if ((posi-2*j+1) <= ln_t) and ((posi-2*j+1) > 0):
				val = val+signal6[0,posj]*signal6[0,posi-2*j]
		signal12[0,posi] = val
	#signal=signal12
	kernel = np.transpose(signal12)*signal12
	x=np.arange(-33,34)
	pan05_mft_up = np.zeros((row,col))
	pan05_mft_up[1:-1:4,1:-1:4] = pan2m_mft
	#start = timer()
	pan05_mft_up_fil = signal.fftconvolve(pan05_mft_up,kernel,mode='same')
	#print('Conv2d signal same takes=')
	#print(timer() - start)
	return pan05_mft_up_fil
######################ajout du code ##########################################
def downsample_perfect(pan2m_perfect):
    #pan2m_mft = [[101,103,105],[111,113,115],[121,123,125]]
    #pan2m_mft=np.asarray([[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13],[0,1,2,3,10,11,12,13]])
    pan2m_perfect=np.array(pan2m_perfect)
    (row0,col0) = pan2m_perfect.shape
    print("taille image entrée pan2m_perfect :",row0,col0,"\n")
    (l_r,l_c)=pan2m_perfect.shape
    f_sz = 4
    n_f = 10  #10
    l_n = f_sz*n_f
    #row = 4*l_r
    #col = 4*l_c
    ln_t = 67
    pos_0 = 33
    signal6 = np.zeros((1,ln_t))
    signal6[0,pos_0] = 1
    signal6[0,pos_0+1] = 2*0.305334091
    signal6[0,pos_0-1] = 2*0.305334091
    signal6[0,pos_0+3] = 2*-0.072698593
    signal6[0,pos_0-3] = 2*-0.072698593
    signal6[0,pos_0+5] = 2*0.021809577
    signal6[0,pos_0-5] = 2*0.021809577
    signal6[0,pos_0+7] = 2*-0.005192756
    signal6[0,pos_0-7] = 2*-0.005192756
    signal6[0,pos_0+9] = 2*0.000807762
    signal6[0,pos_0-9] = 2*0.000807762
    signal6[0,pos_0+11] = 2*-0.000060081
    signal6[0,pos_0-11] = 2*-0.000060081
    signal12 = np.zeros((1,ln_t))
    for i in range(-33,34):
        posi = pos_0+i
        val=0
        for j in range(-11,12):
            posj=pos_0+j;
            if ((posi-2*j+1) <= ln_t) and ((posi-2*j+1) > 0):
                val = val+signal6[0,posj]*signal6[0,posi-2*j]
        signal12[0,posi] = val
    #signal=signal12
    kernel = np.transpose(signal12)*signal12

    #x=np.arange(-33,34)
    #génerer une matrice avec rembourrage
    pan05_perfect_padded =add_sym(pan2m_perfect,f_sz,n_f)
    (l_r_pad,l_c_pad)= pan05_perfect_padded.shape
    print("taille pan05_perfect_padded :",l_r_pad,l_c_pad,"\n")
    pan05_convolution = signal.convolve2d(pan05_perfect_padded, kernel, mode='same', boundary='symm')
    #pan05_convolution = signal.convolve2d(pan2m_perfect, kernel, mode='same', boundary='symm')
    (row2,col2)= pan05_convolution.shape
    print("taille pan05_convolution :",row2,col2,"\n")
    #pan05_mft_up[1:-1:4,1:-1:4] = pan2m_mft
    #start = timer()
    #pan05_mft_up_fil = signal.fftconvolve(pan05_mft_up,kernel,mode='same')
    #print('Conv2d signal same takes=')
    #print(timer() - start)
    #pan05_perfect_down=pan05_convolution[1:-1:4,1:-1:4]
    pan05_perfect_down=pan05_convolution[(l_n):(l_r_pad-l_n),(l_n):(l_c_pad-l_n)]
    (row3,col3)= pan05_perfect_down.shape
    print("taille pan05_perfect_down :",row3,col3,"\n")
    pan05_perfect_down_res = pan05_perfect_down[1:-1:4,1:-1:4]
    (row4,col4)= pan05_perfect_down_res.shape
    print("taille pan05_perfect_down_res :",row4,col4,"\n")
    return pan05_perfect_down_res
###################### fin ajout du code ##########################################

def conv_add_sym(M,PSF,kind):
	f_sz = 4
	n_f  = 10
	l_n = f_sz*n_f
	M_add_sym = add_sym(M,f_sz,n_f)
	#M_add_sym
	#M_add_Blurred
	#start = timer()
	M_add_Blurred = signal.fftconvolve(M_add_sym,PSF,mode='full') 
	#print('Conv2d signal full takes=')
	#print(timer() - start)
	#print(M_add_Blurred[149:154,149:154])
	#M_add_Blurred
	(l_r,l_c) = M_add_Blurred.shape
	M_add_Blurred = M_add_Blurred[(l_n):(l_r-l_n),(l_n):(l_c-l_n)]
	return M_add_Blurred

def downsample_MTF(img,val_pos):
	(row,col) = img.shape
	pos = 0.125	# 1/4 resolution of MS
	#sigma=sqrt(log(val_pos^(-2)))/(pos*2*pi); # ecart-type
	sigma=np.sqrt(np.log(val_pos**(-2)))/(pos*2*np.pi)
	hsize = 33
	tg=np.arange(-(hsize-1)/2,(hsize+1)/2)
	
	#
	gau=np.exp((-tg**2)/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)
	# c bon 
	tg2  = np.arange(1,(hsize+3)/2)
	
	tg2 = tg2 - 0.5
	
	dgs2=0.5 * erf(tg2/(np.sqrt(2)*sigma))
	
	# taille diminue par 1
	gs2 = dgs2[1:len(dgs2)] - dgs2[0:len(dgs2)-1]
	
	gau2= np.concatenate((gs2[::-1], [2*dgs2[0]] ,gs2))
	#print('fct downsample_MTF using hind method')
	gau  = gau2
	gau = gau/gau.sum()
	s= gau.sum()
	gau=np.expand_dims(gau,axis=0)
	PSF = gau.transpose() * gau
	PSF = PSF / PSF.sum()
	pan2m_Blurred = conv_add_sym(img,PSF,'full')
	xr = 1
	xc = 1 
	# on window (1:4,1:4) positionning at pixel (2,2)

	return (pan2m_Blurred[(int((hsize+1)/2+xr-1)):(int((hsize+1)/2+row-1+xr)):4,int((hsize+1)/2+xc-1):int(((hsize+1)/2+col-1+xc)):4])